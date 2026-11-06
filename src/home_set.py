"""A chosen set of plates turned over for the Home page: black marks on white, so they sit on the page rather than as a black block.
Writes site/home/<plate>.gif, a still of each for reduced motion, and site/home.js, which picks one on each load.
Nothing happens on the site until one script tag is added to Home (Page Settings > Advanced):
  <script src="https://catalogue.ramos-saavedra.com/home.js" defer></script>"""
import json, os
import numpy as np
from PIL import Image

PICKS = ['prisms', 'model', 'vee', 'rot_wall', 'doorway', 'censored', 'bones', 'arch', 'mandala', 'slit', 'feedback',
         'beaks', 'dougong', 'spolia', 'same_thing', 'cloche', 'timeline', 'stacked_prisms', 'mended']
OUT = 'site/home'
PAL = [255, 255, 255, 22, 22, 22]
SCRIPT = """(function(){
if(window.self!==window.top)return;
var P=__LIST__,U='https://catalogue.ramos-saavedra.com/',B='https://catalogue.ramos-saavedra.com/home/';
var h=document.querySelector('h1');if(!h)return;var s=h.closest('section');if(!s)return;
var p=P[Math.floor(Math.random()*P.length)],still=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
var a=document.createElement('a');a.href=U;a.className='rs-plate';
var i=document.createElement('img');i.src=B+p.f+(still?'-still.png':'.gif');i.alt=p.a;i.width=i.height=64;i.decoding='async';
var c=document.createElement('span');c.textContent=p.t;a.appendChild(i);a.appendChild(c);
var y=document.createElement('style');y.textContent='.rs-plate{display:block;color:#161616;text-decoration:none;font:400 14px/1.35 "IBM Plex Sans",Arial,sans-serif;z-index:5}.rs-plate img{display:block;image-rendering:pixelated;max-width:none}.rs-plate span{display:block;margin-top:8px}.rs-plate:hover span{text-decoration:underline}';
document.head.appendChild(y);
var o=[].slice.call(s.querySelectorAll('p')).filter(function(x){return x.textContent.trim()==='Start anywhere.'})[0];
function fit(){var w=document.documentElement.clientWidth,r=document.createRange();r.selectNodeContents(h);
var t=r.getBoundingClientRect(),m=parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--sqs-site-gutter'))||0;
var pad=Math.max(t.left,16),room=w-pad-t.right-40,px=Math.min(384,Math.floor(room/64)*64);
if(w>=768&&px>=192){s.style.position='relative';s.appendChild(a);
var top=s.getBoundingClientRect().top,k=o||h;a.style.cssText='position:absolute;right:'+pad+'px;top:'+Math.round(h.getBoundingClientRect().top-top-62)+'px;width:'+px+'px';}
else{px=Math.min(320,Math.floor((w-2*pad)/64)*64);if(px>256)px=256;(o?o.parentElement:h.parentElement).appendChild(a);a.style.cssText='position:static;width:'+px+'px;margin-top:24px';}
i.style.width=i.style.height=px+'px'}
fit();addEventListener('resize',fit);if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fit);
})();
"""


def turn(name):
    im = Image.open(f'site/plates/{name}.gif')
    frames, durs = [], []
    for k in range(im.n_frames):
        im.seek(k)
        a = np.asarray(im.convert('L')) > 128
        frames.append(a.astype(np.uint8))
        durs.append(im.info.get('duration', 100))
    def pic(f):
        i = Image.fromarray(f, 'P')
        i.putpalette(PAL + [0] * (768 - len(PAL)))
        return i
    ims = [pic(f) for f in frames]
    ims[0].save(f'{OUT}/{name}.gif', save_all=True, append_images=ims[1:], duration=durs, loop=0, disposal=1, optimize=False)
    return ims


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    E = {x.get('plate'): x for x in json.load(open('src/entries.json', encoding='utf-8'))}
    items = []
    for n in PICKS:
        ims = turn(n)
        k = E[n]['still']
        ims[min(k, len(ims) - 1) if k >= 0 else k].save(f'{OUT}/{n}-still.png', optimize=True)
        items.append({'f': n, 't': E[n]['text'], 'a': E[n]['alt']})
    open('site/home.js', 'w', encoding='utf-8').write(SCRIPT.replace('__LIST__', json.dumps(items, ensure_ascii=False, separators=(',', ':'))))
    print(len(items))
