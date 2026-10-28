"""Regression checks: a gallery must never publish an incomplete story."""
import copy,json,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALID={'version':3,'rooms':[{'id':'test-room','project':'Test home','title':'Bathroom','evidence':'Matched window, doorway and fixtures.',
    'sequence':[{'file':'test-'+s,'stage':s,'label':s.title(),'width':600,'height':400} for s in ['before','during','after']], 'additional':[]}], 'references':[]}

class GalleryContract(unittest.TestCase):
    def build(self,data):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'scripts').mkdir();(root/'assets/img/hamid').mkdir(parents=True)
            shutil.copy(ROOT/'scripts/build-gallery.py',root/'scripts/build-gallery.py')
            shutil.copy(ROOT/'projects.html',root/'projects.html')
            for p in VALID['rooms'][0]['sequence']:
                for suffix in ['.webp','-thumb.webp']:(root/'assets/img/hamid'/ (p['file']+suffix)).touch()
            (root/'assets/gallery.json').write_text(json.dumps(data),encoding='utf8')
            result=subprocess.run([sys.executable,str(root/'scripts/build-gallery.py')],capture_output=True,text=True)
            return result,(root/'projects.html').read_text(encoding='utf8')

    def test_missing_finished_photo_is_rejected(self):
        data=copy.deepcopy(VALID);data['rooms'][0]['sequence'].pop()
        result,_=self.build(data)
        self.assertNotEqual(result.returncode,0,'Builder published a project without a finished result')
        self.assertIn('before, during and after',result.stderr)

    def test_construction_only_start_is_rejected(self):
        data=copy.deepcopy(VALID);data['rooms'][0]['sequence'].pop(0)
        result,_=self.build(data)
        self.assertNotEqual(result.returncode,0,'Builder published a project without a before photo')
        self.assertIn('before, during and after',result.stderr)

    def test_out_of_order_stages_are_rejected(self):
        data=copy.deepcopy(VALID);data['rooms'][0]['sequence'].reverse()
        result,_=self.build(data)
        self.assertNotEqual(result.returncode,0,'Builder published after before construction')
        self.assertIn('chronological',result.stderr)

    def test_orphan_photos_are_rejected(self):
        data=copy.deepcopy(VALID);data['references']=[{'id':'loose','title':'Loose work','photos':[dict(VALID['rooms'][0]['sequence'][1],file='orphan')]}]
        result,_=self.build(data)
        self.assertNotEqual(result.returncode,0,'Builder published standalone construction photos')
        self.assertIn('standalone',result.stderr)

    def test_complete_album_is_built_in_order(self):
        result,page=self.build(copy.deepcopy(VALID))
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertLess(page.index('test-before.webp'),page.index('test-during.webp'))
        self.assertLess(page.index('test-during.webp'),page.index('test-after.webp'))

if __name__=='__main__':unittest.main(verbosity=2)

