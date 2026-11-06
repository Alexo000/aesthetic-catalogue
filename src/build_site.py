"""Builds site/ from src/entries.json. Run from the repo root: python3 src/plates.py, then python3 src/build_site.py."""
import html, json, os
from PIL import Image

URL = 'https://catalogue.ramos-saavedra.com/'
TITLE = 'Aesthetic Catalogue · Alejandro Ramos Saavedra'
DESC = 'Things I noted as I travelled, over the years: 98 observations, each with a small picture.'
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
    op = f'<a href="https://operations.ramos-saavedra.com/{x["slug"]}/">{e(x["op"])}</a>' if x.get('op') else ''
    pic = plate(x) if 'plate' in x else '<div class="void" role="img" aria-label="Nothing. An empty space the size of a picture."></div>'
    return f'<li>{pic}<div class="cap"><p>{txt(x["text"])}</p>{op}</div></li>'

body = '<ul>' + '\n'.join(item(x) for x in entries) + '</ul>'

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
/* A contact sheet. Everything sits on the plates' own pixel: --m is one plate pixel, and a plate is 64 of them. */
:root {{ color-scheme:dark; --ground:#000; --ink:#f4f3ee; --dim:#8b8a84; --line:#2a2a28;
  --sans:'IBM Plex Sans',Arial,sans-serif; --mono:'IBM Plex Mono',ui-monospace,Menlo,monospace; --cols:2; --plate:168px; --m:2.625px; }}
@media (min-width:640px) {{ :root {{ --cols:3; --plate:192px; --m:3px; }} }}
@media (min-width:980px) {{ :root {{ --cols:4; --plate:224px; --m:3.5px; }} }}
html {{ background:var(--ground); }}
body {{ margin:0; background:var(--ground); color:var(--ink); font:400 15px/1.32 var(--sans);
  padding-block:32px 64px; padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); }}
.wrap {{ width:calc(var(--plate) * var(--cols)); max-width:100%; margin-inline:auto; display:grid; gap:calc(var(--m) * 10); }}
header {{ display:grid; gap:calc(var(--m) * 2); }}
h1 {{ margin:0; font:500 clamp(18px,2vw,22px)/1.3 var(--sans); }}
header p {{ margin:0; color:var(--dim); font-size:clamp(16px,1.8vw,19px); max-width:46ch; }}
ul {{ list-style:none; margin:0; padding:0; display:grid; grid-template-columns:repeat(var(--cols),var(--plate)); }}
li {{ min-width:0; display:flex; flex-direction:column; box-shadow:0 0 0 .5px var(--line); }}
img,.void {{ display:block; width:var(--plate); height:var(--plate); max-width:100%; image-rendering:pixelated; }}
.cap {{ padding:calc(var(--m) * 3) calc(var(--m) * 3) calc(var(--m) * 4); display:grid; gap:calc(var(--m) * 2); align-content:start; flex:1; }}
.cap p {{ margin:0; }}
.cap a {{ font:400 11.5px/1.3 var(--mono); color:var(--dim); justify-self:start; }}
a {{ color:inherit; text-underline-offset:3px; text-decoration-color:var(--line); }}
a:hover {{ color:var(--ink); text-decoration-color:currentColor; }}
a:focus-visible {{ outline:2px solid var(--ink); outline-offset:2px; }}
footer {{ display:grid; gap:6px; color:var(--dim); font:400 14px/1.45 var(--sans); }}
footer p {{ margin:0; max-width:52ch; }}
</style>
<script>
/* Fit the plates to the screen in whole device pixels, so no plate pixel is ever a different size. */
(function(){{var r=document.documentElement;function f(){{var c=getComputedStyle(document.body),d=window.devicePixelRatio||1,w=r.clientWidth-parseFloat(c.paddingLeft)-parseFloat(c.paddingRight),n=w<600?2:w<940?3:w<1500?4:5,p=Math.floor(w/n*d/64)*64/d;r.style.setProperty('--cols',n);r.style.setProperty('--plate',p+'px');r.style.setProperty('--m',p/64+'px')}}document.addEventListener('DOMContentLoaded',f);addEventListener('resize',f)}})();
</script>
</head>
<body>
<div class="wrap">
<header><h1>Aesthetic Catalogue</h1><p>Things I noted as I travelled, over the years.</p></header>
<main>
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
