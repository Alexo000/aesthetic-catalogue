"""Twenty-eight plates worked backwards from Actionary: operations that had no entry, and the observation that shows each."""
from plates5 import *
K=[0,0,0]; W=[244,243,238]
TAU=2*np.pi

def path_pts(P,n=60):
    out=[]
    for (a,b),(c,d) in zip(P,P[1:]):
        for u in np.linspace(0,1,n//(len(P)-1),endpoint=False): out.append((a+(c-a)*u,b+(d-b)*u))
    out.append(P[-1]); return out
def blob(f,x,y,r=1,c=1):
    fill(f,x-r,y-r,x+r-1 if r>1 else x,y+r-1 if r>1 else y,c)
def spread(f,pts,c=1,w=1):
    for x,y in pts:
        fill(f,x,y,x+w-1,y+w-1,c)

def mended():
    bowl=((((xx-C)/27)**2+((yy-20)/30)**2<1)&(yy>=20)&(yy<46))|((np.abs(xx-C)<8)&(yy>=46)&(yy<50))
    tone=np.clip(.42-.34*(xx-C)/27,0,1)
    base=np.where(bowl,dith(tone),0).astype(np.uint8); base[(yy==20)&(np.abs(xx-C)<27)]=1
    A=path_pts([(25,20),(31,28),(26,36),(34,43),(32,49)],40); B=path_pts([(31,28),(41,33),(46,30)],16)
    P=A+[p for p in B]; fr=[];dur=[]
    fr.append(base.copy());dur.append(1300)
    for i in range(6,len(P)+1,6):
        f=base.copy(); spread(f,P[:i],0,2); fr.append(f);dur.append(70)
    for i in range(6,len(P)+1,6):
        f=base.copy(); spread(f,[(a-1,b-1) for a,b in P],0,4); spread(f,P,0,2); spread(f,P[:i],1,2); fr.append(f);dur.append(110)
    dur[-1]=2600
    return fr,dur

def forces():
    def draw(d,top):
        f=blank(); fill(f,0,56,63,56)
        for i in (0,1):
            x=9+i*46; f=poly(f,[(x,44),(x-4,55),(x+4,55)],1)
        for x in range(8,57):
            y=40+d*np.sin(np.pi*(x-8)/48); fill(f,x,y,x,y+2)
        fill(f,25,0,38,top); fill(f,31,0,32,top)
        return f
    fr=[];dur=[]
    for p in np.linspace(14,36,6): fr.append(draw(0,p));dur.append(90)
    for k in np.linspace(0,12,5): fr.append(draw(k,36+k));dur.append(110)
    fr.append(draw(12,48));dur.append(500)
    for u in np.linspace(0,1,7):
        d=12-5*min(u*1.6,1); fr.append(draw(d,48-34*u));dur.append(90)
    dur[-1]=2400
    return fr,dur

def same_thing():
    def idol(cx,base,h):
        m=blank(); m=poly(m,[(cx-h*.14,base-h*.68),(cx+h*.14,base-h*.68),(cx+h*.32,base),(cx-h*.32,base)],1)
        r=h*.2; m=ell(m,cx-r,base-h-.0,cx+r,base-h+2*r,1); return m>0
    S=[(8,13),(19,20),(32,34),(46,26),(57,16)]
    T=[np.ones((G,G),np.uint8),dith(np.full((G,G),.5)),(yy%2==0).astype(np.uint8),((xx+yy)%4==0).astype(np.uint8),None]
    fr=[]
    for t in range(5):
        f=blank(); fill(f,0,52,63,52)
        for i,(cx,h) in enumerate(S):
            m=idol(cx,51,h); k=T[(i+t)%5]
            if k is None:
                e=ndi.binary_erosion(m); f[m&~e]=1
            else: f[m]=k[m]; f[m&~ndi.binary_erosion(m)]=1
        fr.append(f)
    return fr,800

def beaks():
    r=rnd(11); cells=[(i%4,i//4) for i in range(16)]; fr=[];dur=[]; f=blank()
    for y in (14,29,44,59): fill(f,1,y,62,y)
    fr.append(f.copy());dur.append(500)
    for i,(cx,cy) in enumerate(cells):
        x=7+cx*15; y=9+cy*15
        L=3+(i*5%7); d=1+(i*3%3); c=[-2,0,2,3][i%4]
        f=ell(f,x-3,y-3,x+3,y+3,0,1); put(f,x-1,y-1)
        f=poly(f,[(x+3,y-2),(x+3+L,y+c),(x+3,y+d)],1)
        fr.append(f.copy());dur.append(170)
    dur[-1]=2600
    return fr,dur

def timeline():
    P=[(10,12),(26,9),(22,24),(42,16),(52,30),(34,36),(12,34)]
    Q=[(9,50+0)]; fr=[];dur=[]; n=len(P)-1
    for i in range(n):
        for u in np.linspace(0,1,5,endpoint=False):
            x=P[i][0]+(P[i+1][0]-P[i][0])*u; y=P[i][1]+(P[i+1][1]-P[i][1])*u
            f=blank()
            for j in range(i+1):
                A,B=P[j],P[min(j+1,i+1)] if j<i else (x,y)
                for s in np.linspace(0,1,24):
                    a=A[0]+(B[0]-A[0])*s; b=A[1]+(B[1]-A[1])*s
                    if (int(a)+int(b))%3==0: put(f,a,b)
            for p in P[:i+1]: f=ell(f,p[0]-1,p[1]-1,p[0]+1,p[1]+1,1)
            fill(f,x-2,y-2,x+2,y+2)
            fill(f,4,52,59,52)
            for j in range(n+1):
                X=4+j*55/n; fill(f,X,50,X,54)
            X=4+(i+u)*55/n; fill(f,X-1,48,X+1,56)
            fr.append(f);dur.append(120)
    dur[-1]=2200
    return fr,dur

def cloche():
    def draw(lift):
        f=blank(); f=ell(f,8,48,55,53,0,1); fill(f,9,50,54,51,0); fill(f,6,50,57,50)
        f=ell(f,27,41,36,50,1); fill(f,27,47,36,50,0) if False else None or f
        c=(np.hypot((xx-C)/22,(yy-(47-lift))/24)<1)&(yy<=47-lift)
        sh=np.clip(.2+.75*(xx-14)/36,0,1); d=dith(sh)
        f[c]=d[c]; e=c&~ndi.binary_erosion(c); f[e]=1
        fill(f,30,23-lift-3,33,23-lift)
        return f
    fr=[draw(0)];dur=[2000]
    for l in (1,2,4,7,11,15,18,21,23): fr.append(draw(l));dur.append(90)
    dur[-1]=1900
    for l in (21,15,8,3,0): fr.append(draw(l));dur.append(80)
    return fr,dur

def motorbike():
    def wheel(f,x,y,r=5):
        f=ell(f,x-r,y-r,x+r,y+r,0,1); put(f,x,y); return f
    def body():
        f=blank(); fill(f,0,56,63,56)
        f=wheel(f,6,50); f=wheel(f,22,50)
        line(f,6,50,10,36);line(f,10,36,6,34);line(f,10,40,20,40);line(f,20,40,22,50);line(f,12,44,22,44)
        fill(f,11,37,18,39); fill(f,13,28,16,36); f=ell(f,12,22,17,27,1); line(f,14,30,8,34)
        fill(f,27,46,28,47)
        return f
    def carriage(k):
        g=blank(); fill(g,0,47,28,47); fill(g,0,46,1,47); g=wheel(g,20,51,4)
        if k==0:
            fill(g,3,30,27,30); fill(g,4,31,4,46); fill(g,26,31,26,46); figure(g,10,46,1,9); figure(g,19,46,1,9)
        elif k==1: fill(g,3,30,27,46); fill(g,4,33,26,43,0); fill(g,7,36,23,40)
        elif k==2:
            for x in range(3,28,4): fill(g,x,28,x+1,32)
            fill(g,3,28,27,28); fill(g,4,33,4,46); fill(g,26,33,26,46); fill(g,4,39,26,39); put(g,12,37);fill(g,18,36,20,38)
        else:
            for x in (5,12,19): fill(g,x,36,x+4,46); fill(g,x+1,32,x+3,35); fill(g,x+1,38,x+3,44,0)
        return g
    fr=[];dur=[]; B=body()
    def comp(g,dx):
        f=B.copy(); h,w=g.shape
        for y in range(h):
            for x in range(36):
                X=x+dx
                if 0<=X<36 and x<36 and g[y,x] and x+28+0<64 and 28+X<64: f[y,28+X]=1
        return f
    for k in range(4):
        for dx in (32,22,13,6,2,0): fr.append(comp(carriage(k),dx));dur.append(80)
        fr.append(comp(carriage(k),0));dur.append(1300)
        fr[-1]=fr[-1]
        for dx in (2,8,18,30): fr.append(comp(carriage(k),dx));dur.append(80)
    return fr,dur

def dougong():
    P=[((26,47,37,63),1,1),((23,41,40,46),0,1),((16,35,47,40),1,1),((16,29,21,34),0,0),((29,29,34,34),0,0),((42,29,47,34),0,0),
       ((8,23,55,28),1,1),((8,17,13,22),0,0),((29,17,34,22),0,0),((50,17,55,22),0,0),((0,9,63,16),2,1)]
    def piece(f,b,k,dy):
        x0,y0,x1,y1=b; y0+=dy;y1+=dy
        if k==1: fill(f,x0,y0,x1,y1)
        elif k==2:
            m=(xx>=x0)&(xx<=x1)&(yy>=y0)&(yy<=y1); d=dith(np.full((G,G),.5)); f[m]=d[m]; fill(f,x0,y0,x1,y0)
        else:
            fill(f,x0,y0,x1,y1,0); rect(f,x0,y0,x1,y1)
        return f
    fr=[];dur=[]; done=blank()
    fr.append(done.copy());dur.append(400)
    for b,k,_ in P:
        for dy in (-34,-18,-7,-2):
            f=piece(done.copy(),b,k,dy); fr.append(f);dur.append(55)
        done=piece(done,b,k,0); fr.append(done.copy());dur.append(90)
    dur[-1]=2600
    return fr,dur

def dark_sense():
    fr=[];T=22; r=rnd(5)
    for t in range(T):
        a=TAU*t/T; x=C+9*np.cos(a); y=C+6*np.sin(2*a)
        d=np.hypot((xx-x)/11,(yy-y)/15); v=np.exp(-d**4)*.09
        f=(r.random((G,G))<v).astype(np.uint8); fr.append(f)
    return fr,170

def spolia():
    P=[(16,52,47,58,'st'),(20,46,43,51,'so'),(24,28,39,45,'di'),(22,20,41,27,'do'),(17,13,46,19,'la'),(26,5,37,12,'so')]
    def part(f,b):
        x0,y0,x1,y1,k=b
        m=(xx>=x0)&(xx<=x1)&(yy>=y0)&(yy<=y1)
        if k=='so': f[m]=1
        elif k=='st': f[m]=((yy%2)==0)[m]
        elif k=='di': f[m]=dith(np.clip(.8-.65*(xx-x0)/(x1-x0),0,1))[m]
        elif k=='do':
            f[m]=0; rect(f,x0,y0,x1,y1)
            for x in range(x0+2,x1,3): put(f,x,(y0+y1)//2)
        else: f[m]=(((xx+yy)%4==0)|((xx-yy)%4==0))[m]
        return f
    fr=[];dur=[]; done=blank(); fill(done,6,60,57,60)
    fr.append(done.copy());dur.append(500)
    for b in P:
        for dy in (-30,-14,-5):
            f=done.copy(); x0,y0,x1,y1,k=b; f=part(f,(x0+dy,y0,x1+dy,y1,k)) if False else f
            g=part(blank(),b); s=np.roll(g,dy,axis=0); s[:max(0,0)]=0; f[s>0]=1; fr.append(f);dur.append(70)
        done=part(done,b); fr.append(done.copy());dur.append(240)
    dur[-1]=2600
    return fr,dur

def reef():
    v=blank(); v=ell(v,20,20,43,44,1); v=poly(v,[(26,22),(37,22),(35,12),(28,12)],1); fill(v,25,11,38,12); m=v>0
    d=ndi.distance_transform_edt(~m); n=noise2(G,.9,7); fr=[];dur=[]; seabed=(yy>=54)
    for t in range(15):
        a=t/14; f=np.zeros((G,G),np.uint8)
        f[m]=dith(np.where(xx<C,.82,.28))[m]
        g=(d>0)&(d<1+a*12)&(n+(d/(1+a*12))*-1.3>-.55+.2*(1-a))
        g|=(d>0)&(d<1.5+a*1.5)&(a>.05)&(n>-.9+1.2*(1-a))
        f[g]=1; f[seabed]=dith(np.full((G,G),.28))[seabed]; fill(f,0,54,63,54)
        fr.append(f);dur.append(190)
    dur[-1]=2600
    return fr,dur

def wet_statue():
    def base():
        s=blank(); s=ell(s,31,16,45,30,1); s=poly(s,[(33,30),(43,30),(52,56),(24,56)],1); return s
    S=base()>0; fr=[];T=13
    sh=dith(np.clip(.25+.8*(xx-26)/26,0,1))
    for t in range(T):
        f=blank(); f[S]=sh[S]; f[S&~ndi.binary_erosion(S)]=1; fill(f,14,57,61,57)
        a=[-.15,.05,.3,.6,.85,1,1,.9,.6,.3,.1,-.1,-.15][t]
        hx=6;hy=48; L=30; ang=-1.35+1.0*max(a,0)
        ex=hx+L*np.cos(ang); ey=hy+L*np.sin(ang); line(f,hx,hy,ex,ey); fill(f,ex-1,ey-3,ex+3,ey)
        if 5<=t<=10:
            for k in range(5):
                s=(t-5)*.2+k*.17; y=14+s*30
                if y<20: put(f,38+(k%2),y)
            for k in range(14):
                y=19+((t-5)*3+k*3)%36; x=38+[-6,-2,3,7][k%4]+(y-19)*[-.32,-.1,.1,.32][k%4]
                if (k+t)%3: put(f,x,y,0)
        fr.append(f)
    return fr,110

def booth():
    B=[(8,6,17,15),(21,6,30,15),(34,6,43,15),(47,6,56,15)]
    fr=[];dur=[]
    def scene(lit,x,y,tick):
        f=blank(); rect(f,2,2,61,61)
        for i,b in enumerate(B):
            fill(f,b[0],b[1],b[2],b[3]) if i==lit else rect(f,*b)
            fill(f,b[0]+3,b[3],b[2]-3,b[3],0)
        fill(f,x-1,y-1,x,y); return f
    for k,i in enumerate((2,0,3)):
        tx=(B[i][0]+B[i][2])/2
        for u in np.linspace(0,1,12):
            y=56-u*39; x=31+(tx-31)*min(u*1.5,1)
            fr.append(scene(-1,x,y,0));dur.append(80)
        fr.append(scene(i,tx,17,0));dur.append(800)
        for u in np.linspace(1,0,8):
            y=56-u*39; x=31+(tx-31)*min(u*1.5,1)
            fr.append(scene(-1,x,y,0));dur.append(70)
    return fr,dur

def long_tunnel():
    g=dith(np.clip(.34+.1*noise2(G,2.2,3),0,1)).astype(np.uint8)
    room=(xx>=44)&(xx<=59)&(yy>=12)&(yy<=52); slit=(xx<44)&(yy>=30)&(yy<=33)
    g[room]=0;g[slit]=0; ed=(room|slit); bd=ndi.binary_dilation(ed)&~ed; g[bd]=1
    fr=[];T=24
    for t in range(T):
        f=g.copy()
        for k in range(3):
            x=(t*2+k*16)%64-4
            if x<46 and x>=0: fill(f,x,31,x+1,32)
            elif x>=46: pass
        fr.append(f)
    return fr,110

def unclear():
    w=noise3(G,20,2.7,31); fr=[]
    for t in range(20):
        a=w[:,:,t]; a=(a+a[:,::-1])/2; a=a/a.std()
        v=np.clip(.46+.42*a,0,1)*np.clip(1.6-np.hypot((xx-C)/34,(yy-C)/38),0,1)
        f=dith(v); fr.append(np.array(f))
    return fr,230

def ranking():
    H=[46,31,20,12,6]; X=[9,21,33,45,56]; fr=[];dur=[]
    def draw(u):
        f=blank(); fill(f,0,57,63,57)
        for i,(h,x) in enumerate(zip(H,X)):
            H0=14+0*h; hh=H0+(h-H0)*u; w=4
            fill(f,x-w,56-hh,x+w,56)
            for j in range(5-i): put(f,x-4+j*2,60)
        return f
    for u in np.linspace(0,1,12)**1.4: fr.append(draw(u));dur.append(110)
    dur[0]=900;dur[-1]=2800
    return fr,dur

def omikuji():
    def draw(dx,n):
        f=blank(); x=31.5+dx; f=ell(f,x-15,16,x+15,46,1); f=ell(f,x-9,20,x-2,27,0)
        fill(f,x-2,44,x+1,46,0)
        if n:
            fill(f,x-3,46,x+3,46+n)
            for y in range(48,46+n,2): fill(f,x-1,y,x+1,y,0)
        return f
    fr=[];dur=[]
    for t in range(16): fr.append(draw(round(6*np.sin(t*1.45)*(1-t/22)),0));dur.append(70)
    fr.append(draw(0,0));dur.append(450)
    for n in (2,4,6,8,10): fr.append(draw(0,n));dur.append(120)
    dur[-1]=2300
    return fr,dur

def pearl():
    n=noise2(G,2.2,13); fr=[];T=14
    ve=np.abs(np.sin((xx*.7+yy*.45)*.5+2.8*n))<.13
    for t in range(T):
        a=TAU*t/T; lx=-.5+.25*np.cos(a); ly=-.55+.15*np.sin(a); f=blank(); fill(f,0,50,63,50)
        for cx,kind in ((16,0),(47,1)):
            r=13.5; u=(xx-cx)/r; w=(yy-34)/r; d=u*u+w*w; m=d<1
            z=np.sqrt(np.clip(1-d,0,1)); s=np.clip(u*lx+w*ly+z*.72,0,1)**1.1+.2
            g=dith(np.clip(s,0,1))
            f[m]=g[m]
            if kind:
                f[m&ve]=0
            hl=np.hypot(u-lx*.65,w-ly*.65)<.11; f[hl&m]=1
        fr.append(f)
    return fr,130

def electrum():
    m=(xx>=7)&(xx<=56)&(yy>=16)&(yy<=47); fr=[];dur=[]
    w=noise2(G,2.4,17)
    for t,s in enumerate([.5,1.5,3,5,8,12,17,24,34,50,80]):
        step=np.where(xx+ (3*w if t else 0)<C,.92,.14)
        v=ndi.gaussian_filter(step,sigma=s,mode='nearest')
        f=np.zeros((G,G),np.uint8); d=dith(np.clip(v,0,1)); f[m]=d[m]
        rect(f,6,15,57,48); fr.append(f);dur.append(220)
    dur[0]=1300;dur[-1]=2600
    return fr,dur

def bones():
    r=rnd(4)
    cells=[(c,w) for w in range(5) for c in range(4)]; idx=r.permutation(len(cells))
    def draw(gone):
        f=blank(); fill(f,0,59,63,59)
        for c in range(5): fill(f,8+c*12,8,9+c*12,58)
        for w in range(6): fill(f,8,8+w*10,57,9+w*10)
        for i,(c,w) in enumerate(cells):
            if i in gone: continue
            x0=10+c*12;y0=10+w*10
            k=(c+w)%3
            if k==0: fill(f,x0,y0,x0+9,y0+7)
            elif k==1:
                m=(xx>=x0)&(xx<=x0+9)&(yy>=y0)&(yy<=y0+7); f[m]=dith(np.full((G,G),.5))[m]
            else:
                rect(f,x0+1,y0+1,x0+8,y0+6); fill(f,x0+3,y0+3,x0+6,y0+4)
        return f
    fr=[draw(set())];dur=[900]
    g=set()
    for i in idx:
        g.add(int(i)); fr.append(draw(g));dur.append(120)
    dur[-1]=2400
    return fr,dur

def morph():
    th=np.linspace(0,TAU,120,endpoint=False)
    def R(k,t):
        if k==0: return 21/np.maximum(np.abs(np.cos(t)),np.abs(np.sin(t)))
        if k==1: return 25+0*t
        if k==2: return 24+7*np.cos(5*t-np.pi/2)
        return 13/np.maximum(np.cos(np.mod(t+np.pi/2+np.pi/3,TAU/3)-np.pi/3),.05)
    fr=[]
    for k in range(4):
        for u in np.linspace(0,1,8,endpoint=False):
            s=.5-.5*np.cos(np.pi*u); r=(1-s)*R(k,th)+s*R((k+1)%4,th)
            f=poly(blank(),[(C+a*np.cos(b),C+a*np.sin(b)) for a,b in zip(r,th)],1)
            fr.append(f)
    return fr,[420 if i%8==0 else 100 for i in range(32)]

def arch():
    cx,cy=31.5,46; n=9
    def stone(i,f,dy=0):
        a0=np.pi+np.pi*i/n; a1=np.pi+np.pi*(i+1)/n; g=.03
        pts=[(cx+r*np.cos(a),cy+r*np.sin(a)+dy) for r,a in ((14,a0+g),(23,a0+g),(23,a1-g),(14,a1-g))]
        return poly(f,pts,1)
    def wood(f,dy):
        for x,y0,y1 in ((22,36,60),(31,32,60),(41,36,60)):
            fill(f,x,y0+dy,x+1,y1+dy)
        line(f,18,44+dy,45,44+dy); line(f,22,52+dy,31,36+dy); line(f,42,52+dy,31,36+dy)
        for a in np.linspace(np.pi,TAU,40): put(f,cx+13*np.cos(a),cy+13*np.sin(a)+dy)
        return f
    def walls(f):
        fill(f,0,46,8,60);fill(f,55,46,63,60);fill(f,0,61,63,61);return f
    fr=[];dur=[]
    base=wood(walls(blank()),0); done=base.copy(); fr.append(done.copy());dur.append(600)
    for i in (0,8,1,7,2,6,3,5,4):
        done=stone(i,done); fr.append(done.copy());dur.append(150)
    dur[-1]=700
    S=walls(blank())
    for i in range(n): S=stone(i,S)
    for dy in (1,2,5,9,15,23,32):
        f=wood(blank(),dy); f[60:]=0; f=np.maximum(f,S); fr.append(f);dur.append(90)
    fr.append(S.copy());dur.append(2800)
    return fr,dur

def dark_patch():
    fr=[];dur=[]; dark=dith(np.full((G,G),.16)+.1*(noise2(G,2.4,8)))
    clean=dith(np.clip(.86+.07*noise2(G,2.4,9),0,1)); keep=(xx>=39)&(xx<=50)&(yy>=15)&(yy<=24)
    for t in range(15):
        e=(t-1)*8.5; m=(xx+yy*.3+6*noise2(G,2.5,10)<e)&~keep
        f=dark.copy(); f[m]=clean[m]; f[keep]=dark[keep]; fr.append(f);dur.append(150)
    dur[0]=1000;dur[-1]=2800
    return fr,dur

def water_calligraphy():
    g=dith(np.clip(.72+.12*noise2(G,1.5,21),0,1));
    for k in (13,27,41):
        pass
    S=[[(31,8),(31,50),(26,46)],[(27,20),(14,28),(20,32),(9,46)],[(36,18),(46,24),(38,32),(55,47)]]
    fr=[];dur=[]; wet=np.zeros((G,G),bool)
    fr.append(g.copy());dur.append(500)
    for s in S:
        for p in [path_pts(s,30)[:i] for i in range(4,31,4)]:
            w=wet.copy()
            for x,y in p:
                w[max(int(y)-1,0):int(y)+2,max(int(x)-1,0):int(x)+2]=True
            f=g.copy(); f[w]=0; fr.append(f);dur.append(55)
        wet=w
    dur[-1]=900
    d=ndi.distance_transform_edt(wet)+.6*noise2(G,1.2,22)
    for t in range(14):
        a=t*.42; m=wet&(d>a); f=g.copy(); f[m]=0; fr.append(f);dur.append(230)
    dur[-1]=1200
    return fr,dur

def mandala():
    r=np.hypot(xx-C,yy-C); a=np.arctan2(yy-C,xx-C)
    def ring(k):
        if k==0: return r<4
        if k==1: return (r>=6)&(r<11)&(np.cos(8*a)>0)
        if k==2: return (r>=12)&(r<14)
        if k==3: return (r>=15)&(r<21)&(np.cos(12*a)>-.1)&(np.abs(np.mod(r,3)-1)<1.2)
        if k==4: return (r>=22)&(r<24)
        if k==5: return (r>=25)&(r<29)&(np.cos(16*a)>.2)
        return (r>=30)&(r<31.5)
    fr=[];dur=[]; f=blank()
    fr.append(f.copy());dur.append(400)
    for k in range(7):
        f=f.copy(); f[ring(k)]=1; fr.append(f);dur.append(260)
    dur[-1]=1700
    F=f.copy(); n=noise2(G,1.4,5)
    for t in range(1,11):
        e=70-t*9.5; m=(xx*.75+yy*.75+6*n<e); g=np.where(m,F,0).astype(np.uint8)
        fr.append(g);dur.append(120)
    p=blank()
    for t,h in enumerate((2,4,6,7,8)):
        q=fr[-1].copy() if t==0 else p.copy(); q=blank(); q=poly(q,[(C-3-h*1.3,60),(C,60-h),(C+3+h*1.3,60)],1); d=dith(np.full((G,G),.55)); q=np.where(q>0,d,0).astype(np.uint8); fr.append(q);dur.append(150)
    dur[-1]=1500
    return fr,dur

def feedback():
    T=24; buf=np.zeros((G,G)); out=[]
    c=np.array([C,C]); th=np.radians(9); s=1/.84
    M=s*np.array([[np.cos(th),-np.sin(th)],[np.sin(th),np.cos(th)]]); off=c-M.dot(c)
    for t in range(T*3):
        b=ndi.affine_transform(buf,M,offset=off,order=0)
        a=TAU*t/T; f=blank(); rect(f,1,1,62,62); rect(f,2,2,61,61)
        x=C+21*np.cos(a); y=C+21*np.sin(a); fill(f,x-2,y-2,x+2,y+2)
        b=np.maximum(b*(.999),f); buf=b
        if t>=2*T: out.append((b>.5).astype(np.uint8))
    return out,90

def inkblot():
    n=noise2(G,2.0,44); ink=(.75*n+2.2*np.exp(-((xx-29)/13)**2-((yy-C)/19)**2)>1.05)&(xx<=31)&(xx>=9)&(yy>=10)&(yy<=53)
    def sheet(c,show):
        f=blank(); fill(f,8,8,55,55)
        f[ink]=0
        X=32+int(round(c*23))
        if c>=0:
            fill(f,32,8,55,55,0); fill(f,32,8,X,55,1)
            if show and c>0:
                for x in range(32,X+1):
                    sx=int(round(31-(x-32)/max(c,.02)))
                    if 8<=sx<=31: f[8:56,x]=np.where(ink[8:56,sx],0,1)
        else:
            fill(f,X,8,31,55,1); fill(f,32,8,55,55,0)
        return f
    fr=[sheet(1,False)];dur=[1100]
    fr[0]=sheet(1,False)
    for u in np.linspace(0,1,7)[1:]:
        fr.append(sheet(np.cos(np.pi*u),False));dur.append(80)
    dur[-1]=450
    for u in np.linspace(1,0,7)[1:]:
        fr.append(sheet(np.cos(np.pi*u),True) if u<.5 else sheet(np.cos(np.pi*u),False));dur.append(80)
    dur[-1]=2600
    return fr,dur

def slit():
    fr=[];k=.55
    img=np.zeros((G,G),np.uint8); yc=30
    for x in range(G):
        cx=6+k*x+6; ang=x*.14
        for y in range(G):
            dx=x-cx;dy=y-yc; r=np.hypot(dx,dy)
            if 13.5<r<16: img[y,x]=1
            elif r<=13.5:
                a=np.arctan2(dy,dx)+ang
                if abs(np.sin(a*3))<.14 or r<2: img[y,x]=1
    img[52:54,:]=1
    fr=[];dur=[]
    for s in range(0,64,3):
        f=np.zeros((G,G),np.uint8); f[:,:s]=img[:,:s]; f[:,min(s,63)]=1; fr.append(f);dur.append(75)
    fr.append(img.copy());dur.append(2600)
    return fr,dur

SIXTH=dict(mended=mended,forces=forces,same_thing=same_thing,beaks=beaks,timeline=timeline,cloche=cloche,motorbike=motorbike,dougong=dougong,
 dark_sense=dark_sense,spolia=spolia,reef=reef,wet_statue=wet_statue,booth=booth,long_tunnel=long_tunnel,unclear=unclear,ranking=ranking,
 omikuji=omikuji,pearl=pearl,electrum=electrum,bones=bones,morph=morph,arch=arch,dark_patch=dark_patch,water_calligraphy=water_calligraphy,
 mandala=mandala,feedback=feedback,inkblot=inkblot,slit=slit)
if __name__=='__main__':
    import sys,traceback
    for k,fn in SIXTH.items():
        if len(sys.argv)>1 and k not in sys.argv[1:]: continue
        try:
            o=fn(); write(k,o[0],o[1],o[2] if len(o)>2 else None); print(k,len(o[0]) if isinstance(o[0],list) else 1)
        except Exception:
            print('FAIL',k,traceback.format_exc()[-300:])
