from plates_lib import *
R=np.random.default_rng(7)
yy,xx=np.mgrid[0:G,0:G]

def blue(): return np.full((G,G),3,np.uint8)

def light_pierce():
    fr=[]; a=np.array([8.,-2]); b=np.array([50.,66]); L=np.hypot(*(b-a)); d=(b-a)/L; nr=np.array([-d[1],d[0]])
    t=(xx-a[0])*d[0]+(yy-a[1])*d[1]; s=(xx-a[0])*nr[0]+(yy-a[1])*nr[1]
    w=.8+t*.07
    v=np.exp(-(s/w)**2)*np.exp(-t/34)*1.25
    r=np.random.default_rng(1)
    for i in range(10):
        n=r.random((G,G)); fr.append(((v*(.55+.9*n))>r.random((G,G))*.9+.08).astype(np.uint8))
    return fr,110

def dark_substance():
    N=560; x=R.integers(0,G,N); y=R.integers(0,G,N); s=R.choice([1,2],N); fr=[]
    for t in range(G):
        f=blank(); ys=(y+s*t)%G; f[ys,x]=1; f[14:50,18:46]=0; fr.append(f)
    return fr,90

def red_lasers():
    N=2600; x=R.integers(0,G,N); y=R.integers(0,G,N); s=R.choice([1,2],N); fr=[]
    m=blank()
    line(m,-4,10,70,48); line(m,-4,58,70,20)
    for t in range(G):
        f=blank(); ys=(y+s*t)%G; h=blank(); h[ys,x]=1; f[(h>0)&(m>0)]=2; fr.append(f)
    return fr,90

def beam():
    sc=blank()
    def room(s):
        rect(s,18,16,45,47)
        for (a,b),(c,d) in (((18,16),(0,0)),((45,16),(63,0)),((18,47),(0,63)),((45,47),(63,63))): line(s,a,b,c,d)
        for i,x in enumerate(range(0,64,6)): line(s,x,63,18+x*27/63,47)
        for y in (24,32,40): line(s,18,y,45,y)
    room(sc)
    fr=[];dur=[]
    ox,oy=-10,32
    ang=np.arctan2(yy-oy,xx-ox)
    for i,c in enumerate([-.75,-.5,-.25,0,.25,.5,.75]):
        f=(sc*(np.abs(ang-c*.6)<.34)).astype(np.uint8); fr.append(f); dur.append(55)
    fr.append(blank()); dur.append(2100)
    return fr,dur

def mirrors():
    fr=[]; T=28; c=31.5; n=6; sc=.70
    for t in range(T):
        f=blank(); a=2*np.pi*t/T
        px,py=11*np.cos(a),5+3*np.sin(a)
        for i in range(n):
            s=sc**i; h=31*s
            rect(f,c-h,c-h,c+h,c+h)
            x=c+(-1)**i*px*s; y=c+py*s; r=int(round(1.6*s))
            if s>.3: fill(f,round(x)-r,round(y)-r,round(x)+r,round(y)+r)
        fr.append(f)
    return fr,90

def angled():
    fr=[]; T=48; c=31.5; th=np.pi/3
    for t in range(T):
        f=blank(); p=[]
        for k,(r0,ph,w) in enumerate(((10,.3,1),(19,.6,2),(27,.25,1),(24,.85,3))):
            a=2*np.pi*t/T*w
            r=r0+3.5*np.sin(a+k); q=ph+.14*np.sin(a*1+k*2); q=abs(q)%th; p.append((r,q))
        for m in range(3):
            for sg in (1,-1):
                pts=[(c+r*np.cos(sg*q+2*m*th),c+r*np.sin(sg*q+2*m*th)) for r,q in p]
                for (x0,y0),(x1,y1) in zip(pts,pts[1:]): line(f,x0,y0,x1,y1)
        fr.append(f)
    return fr,80

def glass():
    fr=[]; T=32
    lens=[(.0,24,15,9),(.5,46,11,-8)]
    for t in range(T):
        f=blank()
        for x0 in range(1,G,4):
            for y in range(G):
                x=float(x0)
                for ph,cy,sig,A in lens:
                    cx=((t/T+ph)*G)%G
                    dx=((x0-cx+G/2)%G)-G/2; dy=y-cy
                    x+=A*(dx/sig)*np.exp(-(dx*dx+dy*dy)/(sig*sig))
                put(f,x,y)
        fr.append(f)
    return fr,100

def stone():
    fr=[]; 
    for L in range(4):
        f=blank(); y0=0
        for sz,rows in ((16,1),(8,2),(4,4),(2,8)):
            for yy2 in range(sz*rows):
                for x in range(G):
                    a=(x%sz)-(sz-1)/2; b=(yy2%sz)-(sz-1)/2
                    if abs(a)>abs(b): face=1 if a>0 else 3
                    else: face=2 if b>0 else 0
                    lit=face==L or (sz>=8 and face==(L+1)%4 and (x+yy2)%2==0)
                    if sz==2: lit=(x+yy2)%2==0
                    f[y0+yy2,x]=1 if lit else 0
            y0+=sz*rows
        fr.append(f)
    return fr,420

def vee():
    fr=[]; T=44
    for t in range(T):
        f=blank(); vx=32+15*np.sin(2*np.pi*t/T); vy=33
        for x in range(0,64,5): line(f,vx,vy,x,63)
        for x in range(0,64,10): line(f,vx,vy,x,0)
        fr.append(f)
    return fr,80

def sound():
    m=4; n=G-2*m
    def P(mode,X,Y):
        out=0
        for a,b,w in mode: out=out+w*np.cos(np.pi*a*X)*np.cos(np.pi*b*Y)
        return out
    A=[(3,2,1.),(2,3,-.9)]; B=[(4,1,1.),(1,4,.9)]
    N=900; r=np.random.default_rng(3); px=r.random(N); py=r.random(N)
    def step(px,py,al,noise):
        e=.004
        f=lambda x,y:(1-al)*P(A,x,y)+al*P(B,x,y)
        p=f(px,py); gx=(f(px+e,py)-f(px-e,py))/(2*e); gy=(f(px,py+e)-f(px,py-e))/(2*e)
        g=p*gx; h=p*gy
        px=np.clip(px-.0065*g+r.normal(0,noise,N),0,1); py=np.clip(py-.0065*h+r.normal(0,noise,N),0,1)
        return px,py
    for i in range(160): px,py=step(px,py,0,.002)
    fr=[]; T=26
    def draw():
        f=blank(); rect(f,m-1,m-1,G-m,G-m)
        f[(m+py*(n-1)).astype(int),(m+px*(n-1)).astype(int)]=1; return f
    for i in range(10): px,py=step(px,py,0,.0035); fr.append(draw())
    for t in range(T):
        al=.5-.5*np.cos(np.pi*t/(T-1))
        for k in range(3): px,py=step(px,py,al,.0035)
        fr.append(draw())
    for i in range(10): px,py=step(px,py,1,.0035); fr.append(draw())
    return fr+fr[::-1],95

def silence():
    def note(x,y):
        o=[]
        f=blank(); fill(f,x-1,y-1,x+1,y+1); o.append(f)
        f=blank(); rect(f,x-3,y-3,x+3,y+3); put(f,x,y); o.append(f)
        f=blank(); rect(f,x-6,y-6,x+6,y+6); o.append(f)
        f=blank(); 
        for k in range(0,13,3):
            put(f,x-6+k,y-6);put(f,x-6+k,y+6);put(f,x-6,y-6+k);put(f,x+6,y-6+k)
        o.append(f); return o
    fr=note(32,32)+[blank()]+note(32,32)+[blank()]
    dur=[120,120,160,220,5200,120,120,160,220,9000]
    return fr,dur

def comic(n=G,T=24):
    fr=[]; y,x=np.mgrid[0:n,0:n]; c=(n-1)/2; R0=n*.40
    u=(x-c)/R0; v=(y-c)/R0; r2=u*u+v*v; ins=r2<1; z=np.sqrt(np.clip(1-r2,0,1))
    for t in range(T):
        a=2*np.pi*t/T; L=np.array([np.cos(a)*.8,-.45,.55+.3*np.sin(a)]); L/=np.linalg.norm(L)
        b=np.clip(u*L[0]+v*L[1]+z*L[2],0,1)
        f=(dith(b**1.1,CL)*ins).astype(np.uint8); fr.append(f)
    return fr,100

def equidistant():
    f=blank()
    for i in range(7):
        for j in range(7):
            x=8+8*i;y=8+8*j; fill(f,x-1,y-1,x,y)
    return f,0

def heavy():
    seq=[(1,2600),(2,260),(3,1500),(2,260)]
    fr=[];dur=[]
    for g,d in seq:
        f=blank(); yb=38; fill(f,5,6,58,yb-g+1-1); fill(f,14,yb+1,49,57); fr.append(f); dur.append(d)
    return fr,dur

def springs():
    fr=[]; T=48
    O=[(9,26,1,'s'),(21,34,2,'c'),(32,22,3,'s'),(43,38,1,'c'),(55,28,2,'s')]
    for t in range(T):
        f=blank(); f[0:1,:]=1
        for x,b,n,k in O:
            y=b+7*np.sin(2*np.pi*n*t/T+x)
            seg=int(y//3)
            pts=[(x+(2 if i%2 else -2),1+i*(y-1)/seg) for i in range(seg+1)]
            pts[0]=(x,1);pts[-1]=(x,y)
            for (a,c),(d,e) in zip(pts,pts[1:]): line(f,a,c,d,e)
            if k=='s': fill(f,x-3,y,x+3,y+6)
            else:
                for i in range(7): fill(f,x-(3-abs(3-i)),y+i,x+(3-abs(3-i)),y+i)
        fr.append(f)
    return fr,75

def model():
    fr=[]; T=56
    def room(f,x,y,w,t,depth):
        rect(f,x,y,x+w-1,y+w-1)
        bx=x+w*.28;by=y+w*.2;bw=w*.44;bh=w*.46
        rect(f,bx,by,bx+bw,by+bh)
        line(f,x,y,bx,by);line(f,x+w-1,y,bx+bw,by);line(f,x,y+w-1,bx,by+bh);line(f,x+w-1,y+w-1,bx+bw,by+bh)
        # the figure walks the floor
        fx=x+w*(.5+.34*np.sin(t)); fy=y+w*.90; h=w*.15
        fill(f,fx-h*.16,fy-h,fx+h*.16,fy)
        if depth>0:
            s=w*.34; rx=x+(w-s)/2; ry=y+w*.34
            fill(f,rx,ry,rx+s,ry+s,0)
            room(f,rx,ry,s,t,depth-1)
            line(f,rx+s*.3,ry+s,rx+s*.3,y+w*.72);line(f,rx+s*.7,ry+s,rx+s*.7,y+w*.72)
    for i in range(T):
        f=blank(); room(f,1,1,62,2*np.pi*i/T,2); fr.append(f)
    return fr,80

def spiral():
    fr=[]; T=12; c=31.5; x=xx-c;y=yy-c; r=np.hypot(x,y)+.01; th=np.arctan2(y,x)
    for t in range(T):
        v=np.sin(2*th+r*.62-2*np.pi*t/T)
        fr.append(((v>0)&(r<30)).astype(np.uint8))
    return fr,90

def solomon():
    fr=[]; T=14; P=28.
    for t in range(T):
        f=blank(); fill(f,17,3,46,6); fill(f,20,8,43,9); fill(f,17,58,46,61); fill(f,20,55,43,56)
        for y in range(10,55):
            ph=2*np.pi*(y/P-t/T)
            cx=31.5+4.6*np.sin(ph); hw=9.5
            for x in range(int(np.ceil(cx-hw)),int(cx+hw)+1):
                u=np.clip((x-cx)/hw,-1,1); a=np.arcsin(u)/(2*np.pi)      # position round the shaft
                g=np.mod(y/P-t/T+a*1.25,.5)                              # two grooves winding up the shaft
                f[y,x]=0 if g<.11 else 1
        fr.append(f)
    return fr,95

def mound():
    h=blank(); r=np.random.default_rng(5); fr=[]; sand=np.zeros((G,G),bool); moving=[]
    tick=0
    while True:
        sand[0,31+r.integers(-1,2)]=True
        for y in range(G-2,-1,-1):
            xs=np.nonzero(sand[y])[0]; r.shuffle(xs)
            for x in xs:
                if not sand[y+1,x]: sand[y,x]=False;sand[y+1,x]=True
                else:
                    o=[-1,1] if r.random()<.5 else [1,-1]
                    for d in o:
                        if 0<=x+d<G and not sand[y+1,x+d]: sand[y,x]=False;sand[y+1,x+d]=True;break
        tick+=1
        if tick%14==0: fr.append(sand.astype(np.uint8))
        col=sand[:,31]
        hgt=0
        for yy3 in range(G-1,-1,-1):
            if col[yy3]: hgt+=1
            else: break
        if hgt>=48 or tick>2600: break
    dur=[60]*len(fr)+[1600,300]
    fr=fr+[sand.astype(np.uint8),blank()]
    return fr,dur

def drops():
    x=np.arange(G); h0=np.round(44*np.exp(-((x-31.5)/19)**2)+3).astype(float); h=h0.copy()
    r=np.random.default_rng(6); fr=[]; dur=[]
    def pic(h,dy=None,dx=None):
        f=blank()
        for i in range(G):
            f[G-int(h[i]):,i]=1
        if dy is not None and 0<=dy<G: f[max(dy-2,0):dy+1,dx]=1 if dy<G-int(h[dx]) else 0
        return f
    sites=[25,31,36,29,34,22,40]
    for k in range(44):
        dx=sites[k%len(sites)]+r.integers(-1,2)
        top=G-int(h[dx])
        for dy in range(4,top,14): fr.append(pic(h,dy,dx)); dur.append(40)
        # the drop takes earth from where it lands and carries it to the foot of the mound
        for off,amt in ((-1,1),(0,3),(1,1)):
            h[dx+off]=max(h[dx+off]-amt,3)
        toe=r.choice(np.argsort(h)[:10]); h[toe]+=4
        fr.append(pic(h)); dur.append(60)
    fr.append(pic(h)); dur.append(2200)
    return fr,dur

def drift():
    fr=[];dur=[]; r=np.random.default_rng(12); f=blank(); x=np.full(G,3.0); 
    for i,c in enumerate(range(3,62,4)):
        for y in range(G): put(f,x[y]+0,y)
        fr.append(f.copy()); dur.append(240)
        y=r.integers(8,56); w=r.integers(7,16); x=x+4
        x[y:y+w]+=r.choice([-1,1])
    fr.append(f.copy()); dur.append(2400)
    return fr,dur

def sliced():
    T=48; w=noise3(G,T,3.1,4); w2=noise3(G,T,3.1,5); fr=[]; x=(xx-31.5)/31;y=(yy-31.5)/31
    for t in range(T):
        n=w[:,:,t]; m=w2[:,:,t]
        r=np.sqrt((x*1.02)**2+(y*1.18)**2)
        o=.93-r+.07*m                       # the rind
        d=.93-r+.085*n                      # the same depth, disturbed: this is what the bands follow
        b=np.mod(d*9.0,1)<.5
        core=d>.60
        f=((o>0)&b).astype(np.uint8)
        h=dith(np.full((G,G),.5))
        f[core&(o>0)]=h[core&(o>0)]
        fr.append(f)
    return fr,110

def prisms():
    fr=[]; T=60; C=np.array([[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]],float)
    E=[(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
    tilt=.48; ct,st=np.cos(tilt),np.sin(tilt)
    for t in range(T):
        f=blank()
        for s,n in ((19,1),(11.5,-2),(5.8,3)):
            a=(np.pi/2)*n*t/T*1.0; ca,sa=np.cos(a),np.sin(a)
            P=[]
            for x,y,z in C:
                X=x*ca+z*sa; Z=-x*sa+z*ca; Y=y*ct-Z*st; Z2=y*st+Z*ct
                P.append((31.5+s*X,31.5+s*Y))
            for i,j in E: line(f,*P[i],*P[j])
        fr.append(f)
    return fr,75

def glow():
    fr=[]; T=18; r=np.hypot(xx-31.5,yy-31.5)
    for t in range(T):
        k=.5-.5*np.cos(2*np.pi*t/T)
        v=np.clip(1-(r/(15+11*k)),0,1)**1.5*(.62+.3*k)
        fr.append(dith(v))
    return fr,150

def fabric():
    fr=[]; T=16
    X=xx/G; Y=yy/G
    for t in range(T):
        ph=2*np.pi*t/T
        v=np.sin(2*np.pi*(5.2*X + (.2+.95*Y)*np.sin(2*np.pi*(1.2*Y)-ph)*.55 + (.1+.5*Y)*.32*np.sin(2*np.pi*(2.3*Y+.8*X)-2*ph)))
        tone=.5+.5*v
        fr.append(dith(np.clip((tone-.14)*1.5,0,1)**1.2,B8))
    return fr,85

ALL=dict(light_pierce=light_pierce,dark_substance=dark_substance,red_lasers=red_lasers,beam=beam,mirrors=mirrors,angled=angled,glass=glass,stone=stone,vee=vee,sound=sound,silence=silence,comic=comic,equidistant=equidistant,heavy=heavy,springs=springs,model=model,spiral=spiral,solomon=solomon,mound=mound,drops=drops,drift=drift,sliced=sliced,prisms=prisms,glow=glow,fabric=fabric)
if __name__=='__main__':
    import sys,time
    names=sys.argv[1:] or list(ALL)
    for k in names:
        t=time.time(); fr,d=ALL[k](); write(k,fr,d); print(k,len(fr) if isinstance(fr,list) else 1,round(time.time()-t,1))
    write('blue',blue(),0)
