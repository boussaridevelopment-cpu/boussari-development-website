"""Build full, visually reviewed project albums in renovation-stage order."""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
STAGES = ('before', 'during', 'after')
esc = lambda value: html.escape(str(value), quote=True)


def validate(data):
    """Reject incomplete stories and unsequenced photos before publishing."""
    if data.get('references'):
        raise ValueError('Remove standalone photos; publish complete renovation sequences only.')
    if not data.get('rooms'):
        raise ValueError('The gallery needs at least one complete renovation sequence.')
    ids, files = set(), set()
    for room in data['rooms']:
        if room.get('additional'):
            raise ValueError('Remove standalone extra photos; include approved photos in the sequence.')
        for ident in [room['id'], *room.get('aliases', [])]:
            if not re.fullmatch(r'[a-z][a-z0-9-]*', ident) or ident in ids:
                raise ValueError(f'Invalid or duplicate gallery anchor: {ident}')
            ids.add(ident)
        if not room.get('evidence', '').strip():
            raise ValueError(f'{room["id"]}: visual matching evidence is required.')
        phases = [photo['stage'] for photo in room['sequence']]
        if set(phases) != set(STAGES):
            raise ValueError(f'{room["id"]}: each story must include before, during and after.')
        if phases != sorted(phases, key=STAGES.index):
            raise ValueError(f'{room["id"]}: photos must remain in chronological stage order.')
        for photo in room['sequence']:
            stem = photo['file']
            if not re.fullmatch(r'[a-z0-9-]+', stem) or stem in files:
                raise ValueError(f'Invalid or repeated photo: {stem}')
            files.add(stem)
            if not photo.get('label', '').strip() or photo['width'] <= 0 or photo['height'] <= 0:
                raise ValueError(f'{stem}: caption and image dimensions are required.')
            for suffix in ('.webp', '-thumb.webp'):
                if not (ROOT / 'assets/img/hamid' / (stem + suffix)).is_file():
                    raise ValueError(f'Missing gallery image: {stem}{suffix}')


def card(photo, title):
    caption = f'{title} — {photo["stage"].title()}: {photo["label"]}'
    name = esc(photo['file'])
    return (
        f'<figure data-stage="{photo["stage"]}"><a class="photo-open" '
        f'href="assets/img/hamid/{name}.webp" data-caption="{esc(caption)}" '
        f'aria-label="Open {esc(caption)}"><img src="assets/img/hamid/{name}-thumb.webp" '
        f'alt="{esc(photo["label"])}" loading="lazy" decoding="async" '
        f'width="{photo["width"]}" height="{photo["height"]}"></a>'
        f'<figcaption>{esc(photo["label"])}</figcaption></figure>'
    )


def build():
    data = json.loads((ROOT / 'assets/gallery.json').read_text(encoding='utf8'))
    validate(data)
    projects = {}
    for room in data['rooms']:
        projects.setdefault(room['project'], []).append(room)
    album_links, albums, nav = [], [], []
    for title, rooms in projects.items():
        album_id = 'album-' + re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        cover = next((p for p in rooms[0]['sequence'] if p['file'] == rooms[0].get('cover')), rooms[0]['sequence'][-1])
        if cover['stage'] != 'after':
            raise ValueError('Project covers must show completed work.')
        album_links.append(
            f'<a class="album-card" href="#{album_id}"><img '
            f'src="assets/img/hamid/{esc(cover["file"])}-thumb.webp" alt="" '
            f'loading="lazy" decoding="async" width="{cover["width"]}" height="{cover["height"]}">'
            f'<span class="album-card-text"><strong>{esc(title)}</strong>'
            f'<span>{sum(len(r["sequence"]) for r in rooms)} photos &middot; View full project &rarr;</span></span></a>'
        )
        nav.append(f'<a href="#{album_id}">{esc(title)}</a>')
        stories = []
        for room in rooms:
            aliases = ''.join(f'<span class="anchor-alias" id="{alias}" aria-hidden="true"></span>' for alias in room.get('aliases', []))
            columns = []
            for stage_number, stage in enumerate(STAGES, 1):
                photos = ''.join(card(p, room['title']) for p in room['sequence'] if p['stage'] == stage)
                columns.append(f'<section class="story-stage" id="{room["id"]}-{stage}" aria-labelledby="{room["id"]}-{stage}-title"><h3 id="{room["id"]}-{stage}-title"><span>{stage_number:02}</span> {stage.title()}</h3><div class="stage-photos">{photos}</div></section>')
            stage_nav = ''.join(f'<a href="#{room["id"]}-{stage}">{stage.title()}</a>' for stage in STAGES)
            stories.append(
                f'<article class="project-story" id="{room["id"]}">{aliases}'
                f'<nav class="stage-nav" aria-label="{esc(title)} stages">{stage_nav}</nav>'
                f'<div class="story-timeline" data-project="{room["id"]}">{"".join(columns)}</div></article>'
            )
        albums.append(
            f'<section class="project-album" id="{album_id}" aria-labelledby="{album_id}-title">'
            f'<header class="album-heading"><h2 id="{album_id}-title">{esc(title)}</h2></header>'
            + '\n'.join(stories) + '<a class="back-to-albums" href="#before-after">All projects &uarr;</a></section>'
        )
    gallery = (
        '<section class="sec" id="before-after"><div class="wrap">'
        '<nav class="album-index" aria-label="Renovation albums">' + ''.join(album_links) + '</nav>'
        '<div class="project-albums">' + '\n'.join(albums) + '</div></div></section>\n\n'
    )
    path = ROOT / 'projects.html'
    page = path.read_text(encoding='utf8')
    start = page.index('<section class="sec" id="before-after">')
    end = page.index('<section class="cta-band', start)
    page = page[:start] + gallery + page[end:]
    page = re.sub(r'(<main id="main">)\s*<style>.*?</style>', r'\1', page, count=1, flags=re.S)
    page = re.sub(r'<meta name="description" content="[^"]*">',
        '<meta name="description" content="See home and salon renovations from before, through construction, to the finished space. Explore each project in order.">', page)
    page = re.sub(r'<p class="lead">.*?</p>',
        '<p class="lead">Explore each renovation from the original space, through the work, to the finished result.</p>', page, count=1)
    page = re.sub(r'<nav class="story-nav"[^>]*>.*?</nav>',
        '<nav class="story-nav" aria-label="Project transformations">' + ''.join(nav) + '</nav>', page, count=1, flags=re.S)
    if 'assets/css/gallery.css' not in page:
        page = page.replace('</head>', '<link rel="stylesheet" href="assets/css/gallery.css?v=1">\n</head>')
    page = page.replace('gallery.css?v=1', 'gallery.css?v=2')
    page = page.replace('style.css?v=14', 'style.css?v=15').replace('main.js?v=16', 'main.js?v=17')
    page = page.replace('Hamid M. Boussari, Salesperson', 'Hamid Mohammadi-Boussari, Salesperson')
    page = page.replace('Call 416-930-0400 · 24/7 Service', 'Call 416-930-0400 · 24/7 Commercial')
    page = page.replace('Call 416-930-0400 · 24/7 Commercial Service', 'Call 416-930-0400 · 24/7 Commercial')
    path.write_text(page, encoding='utf8', newline='\n')
    print(f'Built {len(projects)} complete project albums, '
          f'{sum(len(r["sequence"]) for r in data["rooms"])} photographs')


if __name__ == '__main__':
    build()
