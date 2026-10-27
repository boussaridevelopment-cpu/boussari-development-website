from pathlib import Path
import json,html,re
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'assets/gallery.json').read_text(encoding='utf8'))
p=ROOT/'projects.html';page=p.read_text(encoding='utf8')
esc=lambda value:html.escape(str(value),quote=True)
total=sum(len(g['photos']) for g in data['renovations'])
articles=[]
for group in data['renovations']:
 stages=list(dict.fromkeys(p['stage'] for p in group['photos']))
 links=''.join(f'<a href="#{group["id"]}-{stage}">{esc(data["stages"][stage])}</a>' for stage in stages)
 sections=[];position=0
 for stage in stages:
  cards=[]
  for photo in [p for p in group['photos'] if p['stage']==stage]:
   position+=1;name=photo['file'];caption=group['title']+' — '+photo['label']
   cards.append(f'<figure><figcaption><span class="photo-number">{position:02}</span> {esc(photo["label"])}</figcaption><a class="photo-open" href="assets/img/hamid/{esc(name)}.webp" data-caption="{esc(caption)}" aria-label="Open {esc(caption)}"><img src="assets/img/hamid/{esc(name)}-thumb.webp" alt="{esc(caption)}" loading="lazy" decoding="async" width="{photo["width"]}" height="{photo["height"]}"></a></figure>')
  sections.append(f'<section class="photo-stage" id="{group["id"]}-{stage}" aria-labelledby="{group["id"]}-{stage}-title"><h3 id="{group["id"]}-{stage}-title">{esc(data["stages"][stage])} <span>({len(cards)} photos)</span></h3><div class="sequence-grid">\n'+ '\n'.join(cards)+'\n</div></section>')
 articles.append(f'<article class="project-story" id="{esc(group["id"])}" data-project="{esc(group["id"])}"><div class="story-heading"><div><p class="eyebrow">{len(group["photos"])} photos</p><h2>{esc(group["title"])}</h2></div><p>{esc(group["description"])}</p></div><nav class="story-nav stage-nav" aria-label="{esc(group["title"])} stages">{links}</nav>\n'+ '\n'.join(sections)+'\n<p class="story-hint">Open any photo to browse this renovation in order.</p></article>')
start=page.index('<section class="sec" id="before-after">');end=page.index('<section class="cta-band',start)
page=page[:start]+'<section class="sec" id="before-after"><div class="wrap project-stories">\n'+'\n'.join(articles)+'\n</div></section>\n\n'+page[end:]
page=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="Browse {total} project photos, grouped by renovation and ordered from before through construction to finished results.">',page)
page=re.sub(r'<p class="lead">.*?</p>', '<p class="lead">Explore each renovation from its original condition through construction to the finished result. Browse every angle and detail, with the available stages shown in order.</p>',page,count=1)
nav=''.join(f'<a href="#{g["id"]}">{esc(g["title"])}</a>' for g in data['renovations'])
page=re.sub(r'<p class="gallery-total">.*?</nav>',f'<p class="gallery-total">{total} photos · {len(data["renovations"])} renovation collections</p><nav class="story-nav" aria-label="Renovation collections">{nav}</nav>',page,count=1,flags=re.S)
css='.photo-stage{margin-top:32px;scroll-margin-top:110px}.photo-stage h3{font-size:1.25rem;color:var(--gold);margin-bottom:20px}.photo-stage h3 span{font-family:Manrope,sans-serif;font-size:.8rem;color:var(--muted)}.stage-nav{margin-bottom:28px}.sequence-grid figcaption{min-height:3em}.photo-open:focus-visible{outline:3px solid var(--gold);outline-offset:4px}'
if css not in page:
 marker=page.index('<style>',page.index('<main'))+len('<style>');page=page[:marker]+css+'\n'+page[marker:]
p.write_text(page,encoding='utf8',newline='\n')
print(f'Built {total} photos in {len(data["renovations"])} renovation collections')
