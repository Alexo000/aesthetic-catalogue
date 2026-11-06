"""The rest of the catalogue on the same 64 by 64 grid. Colour only where the entry names it."""
from plates import *
from PIL import Image as I, ImageDraw as D
from scipy import ndimage as ndi

def pil(f,fn):
    i=I.fromarray(f); fn(D.Draw(i)); return np.asarray(i).copy()
def poly(f,pts,c=1,o=None): return pil(f,lambda d:d.polygon([(float(a),float(b)) for a,b in pts],fill=c,outline=o))
def ell(f,x0,y0,x1,y1,c=1,o=None): return pil(f,lambda d:d.ellipse([x0,y0,x1,y1],fill=c,outline=o))
def figure(f,x,y,c=1,h=9):
    x=int(round(x));y=int(round(y)); fill(f,x-1,y-h,x,y-h+1,c); fill(f,x-1,y-h+3,x,y,c)
def rnd(seed): return np.random.default_rng(seed)
def stip(v,seed=1): return (rnd(seed).random((G,G))<v).astype(np.uint8)
def grain(seed=2,k=1.1,amp=7.,t=.55):
    w=noise2(G,2.6,seed); w2=noise2(G,2.0,seed+1)
    return (np.sin((yy+amp*w+.6*w2)*k)>t).astype(np.uint8)
def vor(n,seed):
    r=rnd(seed); p=r.random((n,2))*G
    d=(yy[...,None]-p[:,0])**2+(xx[...,None]-p[:,1])**2
    lab=d.argmin(-1); e=(lab!=np.roll(lab,1,0))|(lab!=np.roll(lab,1,1)); return lab,e
def ptone(lab,levels,seed):
    r=rnd(seed); lv=r.choice(levels,lab.max()+1); return lv[lab]

# list 1
def neon():
    base=blank(); pts=[(10,46),(10,18),(26,46),(26,18),(38,18),(38,46),(54,46),(54,18)]
    for a,b in zip(pts,pts[1:]): line(base,*a,*b); line(base,a[0]+1,a[1],b[0]+1,b[1])
    d=ndi.distance_transform_edt(base==0); halo=dith(np.exp(-d/5)*.42)
    on=(base|halo).astype(np.uint8); dim=(base&stip(.35,3)).astype(np.uint8)
    return [on,dim,on,dim,on],[1500,70,110,60,2400]
def red_light():
    r=np.hypot(xx-31.5,yy-31.5); return dith(np.clip(1-r/44,0,1)**.8)*2,0
def warm_light():
    w=np.abs(xx-31.5)-(3+.26*yy); v=np.clip(-w/10,0,1)*np.clip(1.05-yy/90,0,1)*.72
    p=np.exp(-(((xx-31.5)/23)**2+((yy-54)/5)**2)*1.6)*.9
    f=dith(np.clip(np.maximum(v,p),0,1)); fill(f,28,0,35,3); return f,0
def strobe():
    def pose(x,a):
        f=blank(); y=46; fill(f,x-1,y-20,x+1,y-18); fill(f,x-1,y-16,x+1,y-8)
        line(f,x,y-15,x+a*8,y-22); line(f,x,y-15,x-a*8,y-8); line(f,x,y-8,x-a*5,y); line(f,x,y-8,x+a*6,y); return f
    fr=[];dur=[]
    for x,a in ((18,1),(27,-1),(36,1),(45,-1)):
        fr+= [pose(x,a),blank()]; dur+=[90,420]
    return fr,dur
def light_substance():
    N=560; r=rnd(8); x=r.integers(0,G,N); y=r.integers(0,G,N); s=r.choice([1,2],N); fr=[]
    for t in range(G):
        f=np.ones((G,G),np.uint8); ys=(y+s*t)%G; f[ys,x]=0; f[14:50,18:46]=1; fr.append(f)
    return fr,90
# list 2
def iridescence():
    fr=[];T=20
    for t in range(T):
        a=2*np.pi*t/T; cx,cy=31.5+7*np.cos(a),31.5+7*np.sin(a)
        A=np.mod(np.hypot(xx-24,yy-31.5)*.95,2)<1; B=np.mod(np.hypot(xx-cx-8,yy-cy)*.95,2)<1
        fr.append((A^B).astype(np.uint8))
    return fr,110
def spray_beam():
    N=2600; r=rnd(4); x=r.integers(0,G,N); y=r.integers(0,G,N); s=r.choice([1,2,2],N); fr=[]
    w=np.abs((xx-8)*.56-(yy-2)*.83)-(1.5+.14*np.hypot(xx-8,yy-2))
    for t in range(G):
        f=blank(); ys=(y+s*t)%G; h=blank(); h[ys,x]=1; f[(h>0)&(w<0)]=1; fr.append(f)
    return fr,85
def proper_light():
    fr=[];dur=[]; r=np.hypot(xx-31.5,yy-31.5); o=(np.abs(xx-31.5)+np.abs(yy-31.5))<9
    for R in (29,25,21,18,15,13.5):
        v=np.clip((R-r)/5,0,1)*.42; f=dith(v); f[o]=1; fr.append(f); dur.append(180)
    fr.append(fr[-1]);dur[-1]=2200
    return fr[:-1],dur
def dust_glow():
    b=stip(.13,5); fr=[]; r=rnd(6)
    for t in range(8):
        k=r.random((G,G))<.06; f=b.copy(); f[k]=1-f[k]*1; f=(f>0).astype(np.uint8); fr.append(f)
    return fr,220
def gold_glow():
    fr=[]; r=np.hypot(xx-31.5,yy-31.5)
    for t in range(8):
        v=np.exp(-r/11)*(.72+.1*np.sin(2*np.pi*t/8)); f=dith(np.clip(v,0,1))
        f=np.array(f); f[23:41,23:41]=1; f[25:39,25:39]=0; f[28:36,28:36]=1; fr.append(f)
    return fr,180
def lamps_temp():
    u=(xx-31.5)/20; v=(yy-31.5)/20; r2=u*u+v*v; ins=r2<1; z=np.sqrt(np.clip(1-r2,0,1))
    a=np.clip(u*-.8+z*.6,0,1); b=np.clip(u*.8+z*.6,0,1)
    A=dith(a,B8); H=(np.mod(yy,3)==0)&(b>.14); H2=(np.mod(yy,2)==0)&(b>.55); Bm=(H|H2)
    def mk(l,rg):
        f=blank()
        if l: f[ins&(A>0)&(u<=.05 if rg else True)]=1; fill(f,1,29,4,34)
        if rg: f[ins&Bm&(u>.05 if l else True)]=1; fill(f,59,29,62,34)
        return f
    return [mk(1,0),mk(0,1),mk(1,1)],[900,900,1400]
def candle():
    fr=[]; r=rnd(3); vase=blank(); vase=poly(vase,[(22,16),(42,16),(38,24),(44,36),(40,46),(24,46),(20,36),(26,24)])
    for t in range(8):
        k=.82+.26*r.random(); d=np.hypot(xx-31.5,(yy-55)*.9); v=np.exp(-d/(19*k))*.95
        f=(dith(v)*(vase>0)).astype(np.uint8)
        fill(f,31,57,32,63); h=r.integers(3,6); fill(f,31,57-h,32,55); put(f,31+r.integers(0,2),57-h-1)
        fr.append(f)
    return fr,130
def mirror_under():
    f=blank(); line(f,4,38,59,38)
    f=poly(f,[(20,20),(44,20),(44,36),(20,36)],0,1)
    g=np.array(f)
    for y in range(40,60,2): line(f,8,y,55,y)
    f[41:58,18:46]=0; rect(f,20,40,44,56)
    for i,(x,y) in enumerate(((26,44),(32,48),(38,44),(38,52),(26,52))): fill(f,x-1,y-1,x+1,y+1)
    return f,0
def mirror_self():
    fr=[];T=24;mx=22
    for t in range(T):
        f=blank(); rect(f,5,8,mx,56); line(f,0,56,63,56)
        x=44+12*np.sin(2*np.pi*t/T); figure(f,x,56,1,14)
        rx=mx-(x-mx)*.55; rx=max(rx,8); figure(f,rx,54,1,10); fr.append(f)
    return fr,90
# list 3
def irregular_reflect():
    w=noise3(G,16,2.9,9); fr=[]
    for t in range(16):
        d=(yy+5.5*w[:,:,t]); fr.append((np.mod(d,7)<1.5).astype(np.uint8))
    return fr,120
def prisms_reflect():
    fr=[];T=12; s=14; h=12
    cx=np.floor(xx/s); fx=xx/s-cx; cy=np.floor(yy/h); fy=yy/h-cy
    up=(fx+fy<1); cid=cx*2+up+cy*3
    for t in range(T):
        tone=.5+.5*np.sin(cid*1.1-2*np.pi*t/T); q=np.round(tone*4)/4
        f=dith(q*.92); e=(np.abs(fx+fy-1)<.05)|(fx<.05)|(fy<.06); f=np.array(f); f[e]=0; fr.append(f)
    return fr,110
def refl_refl():
    fr=[];T=20
    def g(f,x,y,sg):
        fill(f,x-1,y-7,x+1,y+7)
        a,b=sorted((x+sg*1,x+sg*6)); fill(f,a,y-7,b,y-5)
        a,b=sorted((x+sg*1,x+sg*4)); fill(f,a,y-1,b,y+1)
    for t in range(T):
        f=blank(); y=31.5+13*np.sin(2*np.pi*t/T); line(f,21,6,21,57); line(f,42,6,42,57)
        g(f,8,y,1); g(f,34,y,-1); g(f,50,y,1); fr.append(f)
    return fr,90
def mirror_ball():
    fr=[];T=16; u=(xx-31.5)/28; v=(yy-31.5)/28; r2=u*u+v*v; ins=r2<1; z=np.sqrt(np.clip(1-r2,0,1))
    rx=2*z*u; ry=2*z*v; rz=2*z*z-1
    lon=np.arctan2(rx,rz); lat=np.arcsin(np.clip(ry,-1,1))
    for t in range(T):
        c=(np.floor((lon+2*np.pi*t/T/3)/(np.pi/6))+np.floor((lat+1.6)/(np.pi/8)))%2
        fr.append(((c>0)&ins).astype(np.uint8))
    return fr,110
def bevelled():
    fr=[]; b=9
    ins=(xx>=b)&(xx<G-b)&(yy>=b)&(yy<G-b)
    sx=np.where(xx<b,3,np.where(xx>=G-b,-3,0)); sy=np.where(yy<b,3,np.where(yy>=G-b,-3,0))
    for t in range(7):
        g=(np.mod(xx+sx+t,7)==0)|(np.mod(yy+sy+t,7)==0)
        f=g.astype(np.uint8); fr.append(f)
    return fr,130
def stacked_prisms():
    fr=[];T=12
    for t in range(T):
        tri=np.abs(np.mod(yy/8+t/T*2,2)-1); tri2=np.abs(np.mod(yy/5-t/T*2,2)-1)
        d=np.floor(tri*5)+np.floor(tri2*3)
        fr.append((np.mod(xx+d*2,6)<2).astype(np.uint8))
    return fr,110
def fossil():
    n=noise2(G,3.0,12); r=np.hypot(xx-31.5,(yy-31.5)*1.1)+2.4*n; o=r<29
    b=(np.mod(r,3.4)<1.2); c=(np.mod(np.arctan2(yy-31.5,xx-31.5)*9+n,6.28)<.22)
    f=((o&b&~c)).astype(np.uint8); s=stip(.5,7); f=np.array(f); k=(r>=29)&(r<32); f[k]=s[k]; return f,0
def black_concrete():
    f=stip(.045,5)
    for y in (15,31,47):
        f[y,:]=0
        f[y,::3]=1
    for x,y in ((15,8),(47,8),(15,39),(47,39)):
        f=ell(f,x-2,y-2,x+2,y+2,0,1)
    return f,0
def dark_wood():
    w=noise2(G,3.4,2); return (np.mod(yy+9*w+.05*xx,6)<1).astype(np.uint8),0
def dark_cut():
    f,_=dark_wood(); return poly(f,[(36,0),(63,0),(63,63),(48,63)],1),0
# list 4
def marble():
    w=noise2(G,2.2,21); w2=noise2(G,2.2,22); f=((np.abs(w+.5*w2)>.075)).astype(np.uint8)
    f=poly(f,[(32,14),(50,32),(32,50),(14,32)],0); f=poly(f,[(32,21),(43,32),(32,43),(21,32)],1); f=poly(f,[(32,27),(37,32),(32,37),(27,32)],0); return f,0
def marquetry():
    lab,e=vor(24,3); v=ptone(lab,np.array([.0,.2,.45,.7,1.0]),4); f=dith(v); f=np.array(f); f[e]=0; return f,0
def stones_wood():
    f=grain(3,1.0,6.,.72)
    for x,y,a,b,t in ((16,17,9,6,.75),(44,14,7,9,.3),(25,44,8,8,1.),(50,46,9,6,.5)):
        m=((xx-x)/a)**2+((yy-y)/b)**2<1; o=((xx-x)/(a+1.5))**2+((yy-y)/(b+1.5))**2<1
        f[o]=0; f[m]=dith(np.full((G,G),t))[m]
    return f,0
def rough_on_rough():
    g=grain(4,1.1,8.,.3); f=np.array(g); f[:40,:]=0
    m=blank(); m=poly(m,[(13,40),(10,22),(16,9),(30,5),(47,8),(54,20),(50,40)],1)
    s=stip(.55,8); f[m>0]=s[m>0]; f[40,8:56]=1; return f,0
def variations():
    f=blank()
    for i,(d) in enumerate((.2,.45,.7,1.)):
        x=7+i*14; m=blank(); m=poly(m,[(x-5,34),(x+5,34),(x+6,44),(x+3,52),(x-3,52),(x-6,44)],1)
        s=stip(d,9+i); f[m>0]=s[m>0]; line(f,x-5,34,x+5,34)
    return f,0
def milky():
    fr=[];n=noise2(G,3.,31); o=(np.hypot(xx-31.5,(yy-31.5)*1.2)+4*n)<27
    for t in range(12):
        a=2*np.pi*t/12; d=np.hypot(xx-31.5-9*np.cos(a),yy-31.5-7*np.sin(a))
        fr.append((dith(np.clip(.95-d/32,.08,1))*o).astype(np.uint8))
    return fr,160
def faience():
    lab,e=vor(40,6); return (~e).astype(np.uint8),0
def roman_glass():
    n=noise3(G,10,3.0,14); o=blank(); o=poly(o,[(14,10),(46,6),(57,24),(50,50),(26,58),(8,40)],1); fr=[]
    for t in range(10):
        q=np.mod(np.round(n[:,:,t]*3.2)+t*0,5)/4
        fr.append((dith(.12+.8*q)*(o>0)).astype(np.uint8))
    return fr,170
def rough_wood(): return grain(6,1.0,9.,.1),0
# list 5
def melted():
    fr=[]; n=noise2(G,3.,41); T=14
    for t in range(T):
        k=.5-.5*np.cos(2*np.pi*t/T); r=np.hypot(xx-31.5,(yy-26-6*k)*(1.15-.25*k)); o=r+5*n<23
        d=ndi.binary_erosion(o,iterations=2); f=(o&~d).astype(np.uint8)
        f=ell(f,20,16+int(4*k),25,21+int(4*k),1); f=ell(f,35,28+int(5*k),37,30+int(5*k),0,1); put(f,28,34+int(5*k)); put(f,42,20); fr.append(f)
    return fr,120
def paint_glass():
    fr=[];T=18
    for t in range(T):
        k=.5-.5*np.cos(2*np.pi*t/T); f=blank()
        for i,(x,y,ang) in enumerate(((6+10*k,8,0),(20,14+10*k,1),(34-10*k,8,2))):
            m=(xx>=x)&(xx<x+24)&(yy>=y)&(yy<y+44)
            p={0:np.mod(xx+yy,4)==0,1:np.mod(xx-yy,4)==0,2:np.mod(yy,3)==0}[ang]
            f[m&p]=1
            rect(f,x,y,x+23,y+43)
        fr.append(f)
    return fr,110
def smell_space():
    fr=[]; r=rnd(5); T=14
    for t in range(T):
        s=30+8*np.sin(2*np.pi*t/T); d=np.hypot(xx-14,yy-48); v=np.clip(np.exp(-(d/s)**2)*.6,0,1)
        f=(r.random((G,G))<v*.75).astype(np.uint8); fr.append(f)
    return fr,150
def light_space():
    fr=[];T=36; p=((xx-34)/17)**2+((yy-46)/13)**2<1
    for t in range(T):
        x=-6+74*t/T; f=blank(); s=dith(np.full((G,G),.5)); f[p]=s[p]
        h=blank(); figure(h,x,52,1,16); f[(h>0)&p]=0; 
        fr.append(f)
    return fr,90
def temp_space():
    w=noise3(G,20,3.8,15); fr=[]
    for t in range(20):
        fr.append((np.mod(w[:,:,t]*2.6,1)<.1).astype(np.uint8))
    return fr,130
def mirror_struct():
    base=blank(); fill(base,0,8,63,31)
    for x in (2,23,44):
        base=ell(base,x,12,x+17,29,0); fill(base,x,21,x+17,31,0)
    fr=[];dur=[]
    for k in list(range(2,25,4))+[24]:
        f=blank(); f[32-k:32]=base[32-k:32]; line(f,0,32,63,32)
        for y in range(k):
            if y%2==0 or 1: f[33+y]=f[31-y]
        s=(np.mod(yy,2)==0); f[33:][~s[33:]]=0
        fr.append(f);dur.append(200)
    dur[-1]=2400; return fr,dur
def vestibule():
    fr=[];T=26
    for t in range(T):
        f=blank(); fill(f,0,0,20,63); fill(f,43,0,63,63); f[0:,21:43]=0; line(f,21,60,42,60)
        s=dith(np.clip(.55-yy/110,0,1)); m=np.zeros((G,G),bool); m[0:60,21:43]=True; f[m]=s[m]
        h=blank(); figure(h,25+7*np.sin(2*np.pi*t/T)+6,59,1,5); f[h>0]=1; fr.append(f)
    return fr,120
# list 6
def continuation():
    fr=[];T=26; xs=np.arange(0,64)
    for t in range(T):
        f=blank(); ys=44-26*np.sin(xs/63*np.pi*.92)
        for x,y in zip(xs,ys):
            if not 25<=x<=39: fill(f,x,y-2,x,y+2)
        p=(t/T*64)
        fill(f,p,44-26*np.sin(p/63*np.pi*.92)-5,p+1,44-26*np.sin(p/63*np.pi*.92)-4) if not 25<=p<=39 else None
        fr.append(f)
    return fr,90
def monotonous():
    fr=[]
    for t in range(8):
        f=blank()
        for i in range(8):
            x=4+i*8; fill(f,x,24,x+3,39)
        x=4+t*8; fill(f,x,20,x+3,43); fr.append(f)
    return fr,170
def cicadas():
    fr=[]; r=rnd(13); T=26
    for t in range(T):
        k=(t/T)**2; f=(r.random((G,G))<.03+.34*k).astype(np.uint8); f[:, ::2]=0; f[::3,:]=0; fr.append(f)
    return fr,75
def music_silence():
    fr=[];dur=[]; r=rnd(14); h=r.random(40)
    for t in range(14):
        f=blank(); line(f,0,32,63,32)
        for i in range(0,64,2):
            a=int(3+22*abs(np.sin(i*.25+t*.7))*r.random()); fill(f,i,32-a,i,32+a)
        fr.append(f);dur.append(70)
    f=blank(); line(f,0,32,63,32); fr.append(f);dur.append(3200)
    return fr,dur
def poetry():
    r=rnd(15); P=8; rows=8; pat=[]
    for i in range(rows):
        x=6; row=[]
        while x<56:
            w=int(r.integers(2,10)); row.append((x,min(x+w,58))); x+=w+2
        pat.append(row[:int(r.integers(3,8))])
    fr=[]
    for t in range(0,64,2):
        f=blank()
        for i,row in enumerate(pat):
            y=(i*P-t)%64
            for a,b in row:
                fill(f,a,y,b,y+1)
        fr.append(f)
    return fr,120
def gear(f,cx,cy,R,n,ph):
    pts=[]
    for i in range(n*4):
        a=ph+2*np.pi*i/(n*4); r=R if i%4 in (0,1) else R-3
        pts.append((cx+r*np.cos(a),cy+r*np.sin(a)))
    f=poly(f,pts,1); f=ell(f,cx-R+6,cy-R+6,cx+R-6,cy+R-6,0); f=ell(f,cx-1.5,cy-1.5,cx+1.5,cy+1.5,1); return f
def clockwork():
    fr=[];T=12
    for t in range(T):
        k=t/T; f=blank()
        f=gear(f,22,24,16,12,2*np.pi*k/12)
        f=gear(f,47.5,24,11,8,-2*np.pi*k/8+np.pi/8)
        f=gear(f,47.5,46,7.5,6,2*np.pi*k/6)
        a=.5*np.sin(2*np.pi*k); line(f,22,46,22+14*np.sin(a),60-1); fr.append(f)
    return fr,100
def oil_unmixed():
    w=noise2(G,2.8,51); w2=noise2(G,3.0,52)
    v=np.sin((xx*.24+yy*.08+6.5*w)); s=noise2(G,1.0,53)
    return ((v+.25*np.sin((yy+6*w2)*2.6)*(.2+.2*s))>0).astype(np.uint8),0
def white_pencil():
    f=np.full((G,G),4,np.uint8); r=np.hypot(xx-31.5,yy-31.5); t=np.mod(xx+yy,4)==0
    k=rnd(16).random((G,G))<.8
    f[(r<20)&t&k]=1; return f,0
def striped_boxes():
    f=blank(); r=rnd(17)
    for i in range(3):
        for j in range(3):
            x=4+i*19;y=4+j*19; p=int(r.integers(2,5)); o=r.integers(0,2)
            m=np.zeros((G,G),bool); m[y:y+17,x:x+17]=True
            s=(np.mod(yy if o else xx,p)==0); f[m&s]=1; rect(f,x,y,x+16,y+16)
    return f,0
# list 7
def fabric_water():
    fr=[];T=16;X=xx/G;Y=yy/G;r=rnd(18);bx=r.integers(0,G,14);by=r.integers(0,G,14)
    for t in range(T):
        ph=2*np.pi*t/T
        v=np.sin(2*np.pi*(3.2*X+(.25+.8*Y)*np.sin(2*np.pi*(.8*Y)-ph)*.5))
        f=dith(np.clip((.5+.5*v-.2)*1.5,0,1)**1.3)
        f=np.array(f)
        for x,y in zip(bx,by):
            yy2=(y-t*4)%G; f[yy2,x]=1 if f[yy2,x]==0 else 0
        fr.append(f)
    return fr,110
def resin():
    fr=[];T=16
    for t in range(T):
        f=blank(); fill(f,26,58,37,60); fill(f,29,56,34,57)
        ph=2*np.pi*t/T
        for y in range(2,56):
            a=(56-y)/56*11; x=31.5+a*np.sin(y*.21+ph); x2=31.5+a*.7*np.sin(y*.17+ph+1.7)
            if y%2 or y>24: put(f,x,y)
            if y<44: put(f,x2,y)
        fr.append(f)
    return fr,110
def watching():
    fr=[];T=36; r=np.hypot(xx-31.5,yy-31.5); m=r<16
    for t in range(T):
        h=blank(); line(h,0,44,63,44)
        figure(h,(t*2.4)%100-14,44,1,16); figure(h,(t*1.3+34)%100-14,44,1,14)
        f=blank(); f[m]=h[m]; o=(r<17)&(r>=16); f[o]=1; fr.append(f)
    return fr,100
def taste_space():
    fr=[];dur=[]
    angs=[.6,2.4,4.2,5.4]
    for k in range(5):
        f=blank(); rect(f,4,4,59,59); f=ell(f,20,20,43,43,1)
        for a in angs[:k]:
            c,s=np.cos(a),np.sin(a); f=ell(f,31.5+11*c-4,31.5+11*s-4,31.5+11*c+4,31.5+11*s+4,0)
            e=np.array(f); t=27.5/max(abs(c),abs(s)); ex,ey=31.5+t*c,31.5+t*s; fill(e,ex-5,ey-5,ex+5,ey+5,0); f=e
        fr.append(f);dur.append(700)
    dur[-1]=1800
    return fr,dur
def shadows():
    fr=[];T=24
    for t in range(T):
        a=2*np.pi*t/T; f=blank(); dx=20*np.cos(a); dy=9*np.sin(a)
        c=[(22,44),(40,44),(44,50),(26,50)]
        sh=blank(); sh=poly(sh,[c[0],c[1],c[2],c[3],(c[3][0]+dx*1.6,c[3][1]+dy*1.6),(c[2][0]+dx*1.6,c[2][1]+dy*1.6),(c[1][0]+dx*1.6,c[1][1]+dy*1.6),(c[0][0]+dx*1.6,c[0][1]+dy*1.6)],1)
        s=dith(np.full((G,G),.5)); f[sh>0]=s[sh>0]
        f=poly(f,[(22,18),(40,18),(40,44),(22,44)],1); f=poly(f,[(40,18),(44,24),(44,50),(40,44)],0,1); fr.append(f)
    return fr,110
def open_interior():
    fr=[];N=120;r=rnd(19);x=r.integers(0,G,N);y=r.integers(0,G,N);T=16
    for t in range(T):
        f=blank(); fill(f,4,18,16,19); fill(f,47,18,59,19); fill(f,4,18,6,58); fill(f,57,18,59,58); fill(f,4,58,59,59)
        ys=(y+t*4)%64
        for a,b in zip(x,ys):
            if (b<16) or (17<=a<=46 and b<58): put(f,a,b); put(f,a,b+1)
        fr.append(f)
    return fr,85
# list 8
def seat():
    fr=[];dur=[]
    for k in range(10):
        f=blank(); y=18+k*3; f=ell(f,42,y,52,y+10,1); f[46:,:]=0; line(f,0,46,63,46)
        fill(f,12,50,32,51); fill(f,14,52,15,55); fill(f,29,52,30,55); fill(f,19,41,21,49); fill(f,19,37,21,39); fr.append(f); dur.append(420)
    return fr,dur
def scales():
    f=blank()
    def arch(x,y,w,h):
        nonlocal f
        rect(f,x,y+w//2,x+w,y+h); g=f[y:y+w//2+1,x:x+w+1].copy()
        f=ell(f,x,y,x+w,y+w,0,1); f[y+w//2+1:y+h,x+1:x+w]=0
    arch(4,8,28,48); arch(36,24,16,32); arch(55,44,6,12); line(f,0,56,63,56); return f,0
def social():
    fr=[];r=rnd(20);n=10;a=np.linspace(0,2*np.pi,n,endpoint=False);s=r.random((n,2))*G;T=18
    for t in range(T):
        k=t/(T-1); k=k*k*(3-2*k); f=blank(); f=ell(f,20,20,43,43,0,1); f=ell(f,24,24,39,39,0,1)
        for i in range(n):
            tx=31.5+15*np.cos(a[i]);ty=31.5+15*np.sin(a[i]); x=s[i,0]+(tx-s[i,0])*k;y=s[i,1]+(ty-s[i,1])*k; fill(f,x-1,y-1,x,y)
        fr.append(f)
    return fr+[fr[-1]]*0+fr[::-1],100
def helix():
    fr=[];T=14
    for t in range(T):
        f=blank(); ph=2*np.pi*t/T
        for y in range(2,62):
            a=y*.28+ph; x1=31.5+17*np.sin(a); x2=31.5-17*np.sin(a); d=np.cos(a)
            fill(f,x1-(d>0),y,x1+(d>0),y); fill(f,x2-(d<0),y,x2+(d<0),y)
            if y%6==0: line(f,x1,y,x2,y)
        fr.append(f)
    return fr,95
def plinth():
    f=blank(); fill(f,27,14,36,63); f=ell(f,28,5,35,12,1); fill(f,26,13,37,14); figure(f,50,63,1,8); return f,0
def frozen():
    r=rnd(21); ph=r.integers(0,17,G); ln=r.integers(9,14,G); fr=[];dur=[]; off=0; sp=7.
    while sp>.25:
        f=blank()
        for x in range(0,G):
            if x%3==2: continue
            f[:,x]=(np.mod(np.arange(G)-int(off)+ph[x],17)<ln[x]).astype(np.uint8)
        f[:3,:]=1; fr.append(f);dur.append(75); off+=sp; sp*=.86
    dur[-1]=2600; return fr,dur
def extrusion():
    prof=[(10,46),(10,26),(16,26),(16,20),(24,20),(24,26),(30,26),(30,46)]
    fr=[];dur=[]
    for L in list(range(0,29,3)):
        f=blank(); dx,dy=L,-L*.6
        for a,b in zip(prof,prof[1:]+prof[:1]):
            line(f,a[0]+dx,a[1]+dy,b[0]+dx,b[1]+dy)
        for p in prof: line(f,p[0],p[1],p[0]+dx,p[1]+dy)
        f=poly(f,prof,0,1); fr.append(f); dur.append(110)
    dur[-1]=1800; return fr,dur
# list 9
def time_material():
    f=blank(); n=noise2(G,1.6,71)
    for i,t in enumerate((-9,-.75,-.1,.55)):
        x=4+(i%2)*30; y=4+(i//2)*30; m=np.zeros((G,G),bool); m[y:y+26,x:x+26]=True; f[m&(n>t)]=1
    return f,0
def jungle():
    fr=[];T=14; r=rnd(22); L=[(r.integers(0,64),r.integers(0,64),r.integers(3,7),r.integers(0,2)) for _ in range(80)]
    for t in range(T):
        f=blank()
        for x,y,s,c in L:
            d=2*np.sin(2*np.pi*t/T+y*.1); f=ell(f,x+d-s,y-s/2,x+d+s,y+s/2,int(c),1)
        m=(xx<8)|(xx>55)|(yy<8)|(yy>55)|(np.abs(xx-31.5)<1.2)|(np.abs(yy-27.5)<1.2); f=np.array(f); f[m]=0; rect(f,8,8,55,55); line(f,31,8,31,55); line(f,8,27,55,27); fr.append(f)
    return fr,130
def reveal_light():
    fr=[];T=22
    o=np.zeros((G,G),np.uint8); a=np.arctan2(yy-31.5,xx-31.5); r=np.hypot(xx-31.5,yy-31.5)
    o=(((np.mod(a*6/(2*np.pi)+r/14,1)<.5)&(r<25))|(np.abs(r-27)<1)).astype(np.uint8)
    for t in range(T):
        c=-10+84*t/(T-1); m=np.abs(xx-c)<9; f=blank(); f[m]=o[m]; fr.append(f)
    return fr,95
def painted_stone():
    m=blank(); m=poly(m,[(8,40),(12,16),(30,6),(50,12),(58,34),(48,54),(22,56)],1); s=stip(.42,8); f=np.where(m>0,s,0).astype(np.uint8)
    b=(np.abs(yy-.28*xx-22)<5); f[(m>0)&b]=1; b2=(np.abs(yy-.28*xx-34)<1); f[(m>0)&b2]=1; return f,0
def metal_rock():
    pts=[(8,44),(12,18),(30,8),(52,14),(58,36),(46,56),(20,58)]; c=(32,32); fr=[];T=16
    tones=[.15,.5,.8,.3,.6,.1,.4]
    for t in range(T):
        f=blank(); gl=-20+104*t/(T-1)
        for i in range(7):
            a=pts[i];b=pts[(i+1)%7]; m=blank(); m=poly(m,[a,b,c],1); s=dith(np.full((G,G),tones[i])); f[m>0]=s[m>0]
        rock=blank(); rock=poly(rock,pts,1)
        g=(np.abs(xx+yy*.5-gl)<4)&(rock>0); f[g]=1; fr.append(f)
    return fr,95
def gold_leaf():
    n=ndi.gaussian_filter(noise2(G,1.6,81),2.4); n=n/n.std(); gy,gx=np.gradient(n*2.6); fr=[];T=14
    seam=(np.mod(xx,18)==0)|(np.mod(yy,18)==0)
    for t in range(T):
        a=2*np.pi*t/T; b=np.clip(.45+(gx*np.cos(a)+gy*np.sin(a))*1.1,0,1)
        f=dith(b); f=np.array(f); f[seam&(np.mod(xx+yy,3)==0)]=0; fr.append(f)
    return fr,120
def makeup():
    fr=[];dur=[]
    def face(blink):
        f=blank(); f=ell(f,14,6,49,60,0,1)
        if blink: line(f,21,28,28,28); line(f,36,28,43,28)
        else: f=ell(f,22,25,27,30,0,1); f=ell(f,37,25,42,30,0,1); fill(f,24,27,25,28); fill(f,39,27,40,28)
        line(f,31,32,29,40); line(f,29,40,32,40); line(f,26,49,38,49)
        f=poly(f,[(36,22),(46,14),(44,34),(36,31)],1) if 0 else f
        for y in range(16,23):
            line(f,34,y,47-(y-16),y)
        s=dith(np.full((G,G),.5)); m=((xx-40)/5)**2+((yy-40)/4)**2<1; f[m]=s[m]
        return f
    return [face(0),face(1),face(0),face(1)],[2400,120,180,120]
def wood_bronze():
    f=grain(7,1.0,8.,.35); f=np.array(f)
    v=np.clip(.25+.75*np.exp(-((xx+yy*.3-46)/9)**2),0,1); s=dith(v); m=xx>=32; f[m]=s[m]; f[:,31:33]=0; return f,0

def niches():
    # one niche, four lamps: the only thing that changes is the texture of the light
    f=blank(); pats=[lambda:(np.mod(xx,2)==0)&(np.mod(yy,2)==0),lambda:np.mod(xx+yy,2)==0,lambda:np.mod(yy,2)==0,lambda:np.ones((G,G),bool)]
    for i,p in enumerate(pats):
        x=3+i*15; m=blank(); m=ell(m,x,10,x+11,21,1); fill(m,x,16,x+11,54)
        f[(m>0)&p()]=1
    return f,0

MORE=dict(niches=niches,neon=neon,red_light=red_light,warm_light=warm_light,strobe=strobe,light_substance=light_substance,iridescence=iridescence,spray_beam=spray_beam,proper_light=proper_light,dust_glow=dust_glow,gold_glow=gold_glow,lamps_temp=lamps_temp,candle=candle,mirror_under=mirror_under,mirror_self=mirror_self,irregular_reflect=irregular_reflect,prisms_reflect=prisms_reflect,refl_refl=refl_refl,mirror_ball=mirror_ball,bevelled=bevelled,stacked_prisms=stacked_prisms,fossil=fossil,black_concrete=black_concrete,dark_wood=dark_wood,dark_cut=dark_cut,marble=marble,marquetry=marquetry,stones_wood=stones_wood,rough_on_rough=rough_on_rough,variations=variations,milky=milky,faience=faience,roman_glass=roman_glass,rough_wood=rough_wood,melted=melted,paint_glass=paint_glass,smell_space=smell_space,light_space=light_space,temp_space=temp_space,mirror_struct=mirror_struct,vestibule=vestibule,continuation=continuation,monotonous=monotonous,cicadas=cicadas,music_silence=music_silence,poetry=poetry,clockwork=clockwork,oil_unmixed=oil_unmixed,white_pencil=white_pencil,striped_boxes=striped_boxes,fabric_water=fabric_water,resin=resin,watching=watching,taste_space=taste_space,shadows=shadows,open_interior=open_interior,seat=seat,scales=scales,social=social,helix=helix,plinth=plinth,frozen=frozen,extrusion=extrusion,time_material=time_material,jungle=jungle,reveal_light=reveal_light,painted_stone=painted_stone,metal_rock=metal_rock,gold_leaf=gold_leaf,makeup=makeup,wood_bronze=wood_bronze)
if __name__=='__main__':
    import sys,traceback
    bad=[]
    for k,fn in MORE.items():
        if len(sys.argv)>1 and k not in sys.argv[1:]: continue
        try:
            fr,d=fn(); write(k,fr,d)
        except Exception as e:
            bad.append((k,repr(e)[:90]))
    print(len(MORE),'bad',bad)
