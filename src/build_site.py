"""Builds site/ from src/entries.json. Run from the repo root: python3 src/plates.py, then python3 src/build_site.py."""
import html, json, os
from PIL import Image

URL = 'https://catalogue.ramos-saavedra.com/'
TITLE = 'Aesthetic Catalogue · Alejandro Ramos Saavedra'
DESC = 'Things I noted as I travelled, over the years: 98 observations, some with a small moving picture.'
e = lambda s: html.escape(s, quote=True)
txt = lambda s: html.escape(s, quote=False)
entries = json.load(open('src/entries.json', encoding='utf-8'))

def still(name, frame):
    """A still of each GIF, served to people who ask their device for reduced motion."""
    im = Image.open(f'site/plates/{name}.gif')
    im.seek(min(frame, im.n_frames - 1) if frame >= 0 else im.n_frames + frame)
    im.convert('P', colors=4).save(f'site/plates/{name}-still.png', optimize=True)

def plate(x):
    n, alt = x['plate'], e(x['alt'])
    if os.path.exists(f'site/plates/{n}.gif'):
        still(n, x['still'])
        return (f'<picture><source media="(prefers-reduced-motion: reduce)" srcset="plates/{n}-still.png">'
                f'<img src="plates/{n}.gif" width="64" height="64" alt="{alt}" loading="lazy" decoding="async"></picture>')
    return f'<img src="plates/{n}.png" width="64" height="64" alt="{alt}" loading="lazy" decoding="async">'

def item(x):
    cap = f'<a href="https://operations.ramos-saavedra.com/{x["slug"]}/">{e(x["op"])}</a>' if x.get('op') else ''
    if 'plate' in x:
        fig = f'<figure>{plate(x)}<figcaption>{cap}</figcaption></figure>'
    elif x.get('void'):
        fig = f'<figure><div class="void" role="img" aria-label="Nothing. An empty space the size of a picture."></div><figcaption>{cap}</figcaption></figure>'
    else:
        fig = ''
    return f'<li><p>{txt(x["text"])}</p>{fig}</li>'

lists = {}
for x in entries:
    lists.setdefault(x['list'], []).append(item(x))
body = '\n'.join('<ul>' + ''.join(v) + '</ul>' for v in lists.values())

page = f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(TITLE)}</title>
<meta name="description" content="{e(DESC)}">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Ramos Saavedra">
<meta property="og:title" content="Aesthetic Catalogue">
<meta property="og:description" content="{e(DESC)}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="{URL}share.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#000000">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&family=IBM+Plex+Sans:wght@400;500&display=swap">
<script>window.goatcounter={{path:function(p){{return location.host+p}}}}</script>
<script data-goatcounter="https://alexo000.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
<style>
/* One long black room. The words stay still; a picture is one line of the list given a body. Every picture shares a 64 by 64 grid, scaled by whole numbers. */
:root {{ color-scheme:dark; --ground:#000; --ink:#f4f3ee; --dim:#8b8a84; --line:#2a2a28;
  --sans:'IBM Plex Sans',Arial,sans-serif; --mono:'IBM Plex Mono',ui-monospace,Menlo,monospace; --plate:320px; }}
html {{ background:var(--ground); }}
body {{ margin:0; background:var(--ground); color:var(--ink); font:400 18px/1.36 var(--sans);
  padding-block:32px 64px; padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); }}
.wrap {{ max-width:640px; margin-inline:auto; display:grid; gap:64px; }}
header {{ display:grid; gap:10px; }}
h1 {{ margin:0; font:500 18px/1.3 var(--sans); }}
header p {{ margin:0; color:var(--dim); max-width:46ch; }}
ul {{ list-style:none; margin:0; padding:0; display:grid; gap:12px; }}
li {{ display:grid; min-width:0; }}
li p {{ margin:0; max-width:52ch; }}
figure {{ margin:16px 0 28px; display:grid; gap:9px; justify-items:start; }}
figcaption {{ font:400 13px/1.3 var(--mono); color:var(--dim); min-height:17px; }}
a {{ color:inherit; text-underline-offset:3px; text-decoration-color:var(--line); }}
a:hover {{ color:var(--ink); text-decoration-color:currentColor; }}
a:focus-visible {{ outline:2px solid var(--ink); outline-offset:3px; }}
img,.void {{ display:block; width:var(--plate); height:var(--plate); max-width:100%; image-rendering:pixelated; }}
footer {{ display:grid; gap:6px; border-top:1px solid var(--line); padding-top:20px; color:var(--dim); font:400 14px/1.45 var(--sans); }}
footer p {{ margin:0; max-width:52ch; }}
@media (min-width:700px) {{ :root {{ --plate:448px; }} body {{ font-size:21px; padding-block:64px 88px; }} h1 {{ font-size:21px; }} ul {{ gap:14px; }} figure {{ margin:20px 0 36px; }} .wrap {{ gap:88px; }} }}
@media (max-width:351px) {{ :root {{ --plate:256px; }} }}
</style>
</head>
<body>
<div class="wrap">
<header><h1>Aesthetic Catalogue</h1><p>Things I noted as I travelled, over the years.</p></header>
<main style="display:grid;gap:inherit">
{body}
</main>
<footer>
<p>The small names under the pictures are moves from <a href="https://operations.ramos-saavedra.com">Actionary</a>.</p>
<p>© 2026 <a href="https://www.ramos-saavedra.com/">Alejandro Ramos Saavedra</a> · <a href="https://www.ramos-saavedra.com/privacy">Privacy</a></p>
</footer>
</div>
</body>
</html>
'''
open('site/index.html', 'w', encoding='utf-8').write(page)
open('site/robots.txt', 'w').write(f'User-agent: *\nAllow: /\nSitemap: {URL}sitemap.xml\n')
open('site/sitemap.xml', 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{URL}</loc></url></urlset>\n')
