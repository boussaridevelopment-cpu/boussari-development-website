"""Build the static room-by-room gallery from the reviewed image manifest."""
from pathlib import Path
import json,html,re
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'assets/gallery.json').read_text(encoding='utf8'))
page=(ROOT/'projects.html').read_text(encoding='utf8');esc=lambda s:html.escape(str(s),quote=True)
rooms=data['rooms'];references=data['references']
total=sum(len(r['sequence'])+len(r['additional']) for r in rooms)+sum(len(r['photos']) for r in references)
assert total==len({p['file'] for r in rooms for p in r['sequence']+r['additional']}|{p['file'] for r in references for p in r['photos']})
def card(p,title):
 caption=esc(title+' — '+p['label']);name=esc(p['file'])
 return f'<figure><figcaption>{esc(p["label"])}</figcaption><a class="photo-open" href="assets/img/hamid/{name}.webp" data-caption="{caption}" aria-label="Open {caption}"><img src="assets/img/hamid/{name}-thumb.webp" alt="{caption}" loading="lazy" decoding="async" width="{p["width"]}" height="{p["height"]}"></a></figure>'
articles=[]
for r in rooms:
 primary='\n'.join(card(p,r['title']) for p in r['sequence'])
 article=f'<article class="project-story" id="{r["id"]}"><header class="story-heading"><p class="eyebrow">{esc(r["project"])}</p><h2>{esc(r["title"])}</h2></header><div class="sequence-grid primary-sequence" style="--columns:{len(r["sequence"])}" data-project="{r["id"]}-sequence">\n{primary}\n</div>'
 extras=[p for p in r['additional'] if p['stage']!='comparison'];comparisons=[p for p in r['additional'] if p['stage']=='comparison']
 if extras:
  content=[]
  for stage,label in [('before','Before — more views'),('during','During renovation — more views'),('after','Finished details — more views')]:
   photos=[p for p in extras if p['stage']==stage]
   if photos:content.append(f'<h3>{label}</h3><div class="sequence-grid more-grid">'+'\n'.join(card(p,r['title']) for p in photos)+'</div>')
  article+=f'<details class="room-details"><summary>More photos of this space ({len(extras)})</summary><div data-project="{r["id"]}-details">'+''.join(content)+'</div></details>'
 if comparisons:
  article+=f'<details class="room-details"><summary>Original comparison collages ({len(comparisons)})</summary><div class="sequence-grid more-grid" data-project="{r["id"]}-collages">'+''.join(card(p,r['title']) for p in comparisons)+'</div></details>'
 articles.append(article+'</article>')
archive_count=sum(len(r['photos']) for r in references)
archive=f'<section class="project-story additional-views" id="additional-views"><header class="story-heading"><p class="eyebrow">{archive_count} individual photos</p><h2>Additional project views</h2><p>Construction details and other views without a confirmed matching sequence.</p></header>'
for r in references:
 archive+=f'<details class="room-details"><summary>{esc(r["title"])} ({len(r["photos"])})</summary><div class="sequence-grid more-grid" data-project="{r["id"]}">'+''.join(card(p,r['title']) for p in r['photos'])+'</div></details>'
archive+='</section>'
start=page.index('<section class="sec" id="before-after">');end=page.index('<section class="cta-band',start)
page=page[:start]+'<section class="sec" id="before-after"><div class="wrap project-stories">\n'+'\n'.join(articles)+archive+'\n</div></section>\n\n'+page[end:]
css='''
.project-stories{display:grid;gap:64px}.project-story{scroll-margin-top:110px;border-top:1px solid var(--line);padding-top:28px}.story-heading{margin-bottom:24px}.story-heading h2{font-size:clamp(1.7rem,3vw,2.5rem);margin:0}.story-heading p{max-width:680px;color:var(--silver)}.story-heading .eyebrow{font-size:.75rem;color:var(--gold);margin-bottom:10px}.sequence-grid{display:grid;grid-template-columns:repeat(var(--columns,3),minmax(0,1fr));gap:24px}.sequence-grid figure{margin:0;min-width:0}.sequence-grid figcaption{font-size:.86rem;line-height:1.5;min-height:3em;margin-bottom:10px;color:var(--gold)}.sequence-grid img{display:block;width:100%;height:320px;object-fit:contain;background:#101820}.sequence-grid .photo-open{border:1px solid var(--line)}.photo-open:focus-visible{outline:3px solid var(--gold);outline-offset:4px}.story-nav{display:flex;gap:8px;flex-wrap:wrap;margin-top:28px}.story-nav a{border:1px solid var(--line);padding:8px 12px;font-size:.8rem}.gallery-total{color:var(--gold);font-size:.8rem;letter-spacing:.06em;margin-top:22px}.room-details{margin-top:20px;border-top:1px solid var(--line)}.room-details summary{cursor:pointer;padding:18px 0;color:var(--silver);font-size:.9rem}.room-details summary:hover{color:var(--gold)}.room-details h3{font-size:1rem;color:var(--gold);margin:28px 0 18px}.more-grid{margin:10px 0 28px}.more-grid img{height:240px}.more-grid figcaption{font-size:.78rem}.additional-views{margin-top:20px}@media(max-width:900px){.more-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.primary-sequence{gap:14px}}@media(max-width:650px){.sequence-grid{grid-template-columns:1fr}.sequence-grid figcaption{min-height:0}.primary-sequence{gap:28px}.project-stories{gap:42px}.sequence-grid img{height:320px}.more-grid img{height:280px}}
'''
main=page.index('<main id="main">');page=page[:main]+re.sub(r'<style>.*?</style>',lambda _: '<style>'+css+'</style>',page[main:],count=1,flags=re.S)
page=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="See {len(rooms)} matching room and exterior transformations, with before, construction and finished views. Browse all {total} project photos.">',page)
page=re.sub(r'<p class="lead">.*?</p>','<p class="lead">See each space change, from its earlier condition through the work to the result. Each row follows one room or exterior. Open the extra views beneath it for more photos of that space.</p>',page,count=1)
project_links={}
for r in rooms:project_links.setdefault(r['project'],r['id'])
nav=''.join(f'<a href="#{ident}">{esc(title)}</a>' for title,ident in project_links.items())+'<a href="#additional-views">Additional views</a>'
page=re.sub(r'<p class="gallery-total">.*?</nav>',f'<p class="gallery-total">{len(rooms)} matching spaces · {total} project photos</p><nav class="story-nav" aria-label="Project transformations">{nav}</nav>',page,count=1,flags=re.S)
(ROOT/'projects.html').write_text(page,encoding='utf8',newline='\n')
print(f'Built {len(rooms)} room sequences and {total} photos')
