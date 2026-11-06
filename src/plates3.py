"""Twenty more from the Keep list, on the same 64 by 64 grid. Several use a viewpoint the first set did not: moving forward, zooming, parallax, changing projection."""
from plates2 import *

def hole_light():
    fr=[];T=18; r=np.hypot(xx-31.5,yy-31.5)
    for t in range(T):
        R=8+4*(.5-.5*np.cos(2*np.pi*t/T)); v=np.clip(np.exp(-(r-R)/6)*.85,0,1)
        f=dith(v); f=np.array(f); f[r<R]=1; fr.append(f)
    return fr,130
def red_dot():
    f=blank(); fill(f,31,31,32,32,2); return f,0
def slow_cloud():
    w=noise3(G,18,3.2,25); fr=[]
    for t in range(18):
        d=5*np.sin(2*np.pi*t/18)
        v=np.exp(-((xx-31.5-d)/19)**2-((yy-30)/9)**2)*1.1+.28*w[:,:,t]-.28
        f=dith(np.clip(v,0,1)); f=np.array(f); rect(f,3,3,60,60); fr.append(f)
    return fr,280
def tunnel():
    fr=[];T=10;q=.72
    for t in range(T):
        f=blank()
        for a,b in ((0,0),(63,0),(0,63),(63,63)): line(f,a,b,31.5+(a-31.5)*.1,31.5+(b-31.5)*.1)
        for i in range(-1,10):
            r=36*q**(i+1-t/T)
            if r>1.5: f=ell(f,31.5-r*.9,31.5-r*.9,31.5+r*.9,31.5+r*.9,None,1) if False else f; rect(f,31.5-r,31.5-r,31.5+r,31.5+r)
        fr.append(f)
    return fr,75
def spiral_space():
    a=8/(2*np.pi); fr=[];dur=[]; th=np.linspace(0,7*np.pi,500); base=blank()
    for s in th:
        r=2+a*s; put(base,31.5+r*np.cos(s),31.5+r*np.sin(s))
    pts=[(2+a*s+4,s) for s in np.linspace(7*np.pi-.4,.6,42)]
    for r,s in pts:
        f=np.array(base); x=31.5+r*np.cos(s); y=31.5+r*np.sin(s); fill(f,x-1,y-1,x+1,y+1); fr.append(f); dur.append(95)
    f=np.array(base); fill(f,31,31,32,32); fr.append(f); dur.append(400)
    fr.append(np.array(base)); dur.append(1400)
    return fr,dur
def peephole():
    fr=[];T=24; H=[(14,32),(32,32),(50,32)]; mask=np.zeros((G,G),bool)
    for x,y in H: mask|=np.hypot(xx-x,yy-y)<8
    for t in range(T):
        d=6*np.sin(2*np.pi*t/T)
        s=((np.mod(xx+d,10)<3)&(np.mod(yy+1.3*d,10)<3))
        f=np.ones((G,G),np.uint8); f[mask]=0; f[mask&s]=1; fr.append(f)
    return fr,95
def compartments():
    R=[27,19,12,6]; fr=[];dur=[]
    def draw(k,off):
        f=blank()
        for i,r in enumerate(R):
            if i<=k: rect(f,31.5-r,31.5-r,31.5+r,31.5+r)
        if k>=len(R)-1 and off>=70: fill(f,30,30,33,33)
        if k<len(R):
            r=R[k]-1; a=31.5-r+off; g=np.array(f); fill(g,a,31.5-r,31.5+r+off,31.5+r,1)
            m=np.zeros((G,G),bool); m[int(31.5-r):int(31.5+r)+1,int(31.5-r):int(31.5+r)+1]=True; f[m]=g[m]
        return f
    for k in range(len(R)):
        for o in (0,10,20,32,46,70):
            fr.append(draw(k,o)); dur.append(600 if o==0 else 80)
    dur[-1]=1700; return fr,dur
def cabinets():
    fr=[];T=12
    for t in range(T):
        f=blank(); a0=np.pi/3*t/T
        f=ell(f,10,5,53,13,0,1); f=ell(f,10,51,53,59,0,1); f[55:60,:]=np.where(yy[55:60,:]>=55,0,0); f=ell(f,10,51,53,59,0,1); f[:55,:]=np.where(f[:55,:]>0,f[:55,:],0)
        line(f,10,9,10,55); line(f,53,9,53,55)
        for y in (21,33,45): 
            for x in range(10,54):
                u=(x-31.5)/21.5; put(f,x,y+3*np.sqrt(max(1-u*u,0)))
        for k in range(6):
            a=a0+k*np.pi/3
            if np.cos(a)>0:
                x=31.5+21.5*np.sin(a); line(f,x,12,x,57)
                for y in (15,27,39,50):
                    fill(f,x+2,y-2,x+4,y+1) if abs(np.sin(a))<.7 else None
        fr.append(f)
    return fr,110
def smoke_stone():
    fr=[];T=16; st=[(14,56),(11,44),(20,36),(34,34),(46,38),(52,50),(48,57)]
    base=blank(); base=poly(base,st,1); s=stip(.55,3); b=np.where(base>0,s,0).astype(np.uint8); b=poly(b,[],1) if False else b
    for a,c in zip(st,st[1:]+st[:1]): line(b,*a,*c)
    for t in range(T):
        f=np.array(b); ph=2*np.pi*t/T
        for x0,k in ((26,.2),(32,.17),(38,.23)):
            for y in range(4,36):
                a=(36-y)/36*8; x=x0+a*np.sin(y*k+ph+x0); 
                if (y+t)%3: put(f,x,y)
        fr.append(f)
    return fr,110
def phi():
    pts=[(x,10) for x in range(8,56,6)]+[(56,y) for y in range(10,54,6)]+[(x,54) for x in range(56,8,-6)]+[(8,y) for y in range(54,10,-6)]
    fr=[];n=len(pts)
    for t in range(n):
        f=blank()
        for i,(x,y) in enumerate(pts):
            if (i-t)%n in (0,1,2): fill(f,x-1,y-1,x+1,y+1)
            else: put(f,x,y)
        fr.append(f)
    return fr,75
def double_sym():
    w=noise3(G,20,2.0,26); fr=[]; ax=np.abs(xx-31.5).astype(int); ay=np.abs(yy-31.5).astype(int)
    for t in range(20): fr.append((w[ay,ax,t]>.1).astype(np.uint8))
    return fr,140
def almost():
    fr=[];r=rnd(27); pos=[(int(a),int(b)) for a,b in r.integers(0,7,(14,2))]
    g=np.zeros((5,5),np.uint8); g[0,:]=1; g[:,0]=1; g[4,:3]=1; h=g[:,::-1]
    for p in pos:
        f=blank()
        for i in range(7):
            for j in range(7):
                x=5+i*8;y=5+j*8; f[y:y+5,x:x+5]=h if (i,j)==p else g
        fr.append(f)
    return fr,380
def thin():
    fr=[];T=26; s=np.linspace(0,1,400)
    for t in range(T):
        f=blank(); a=t/T
        for k in (0,1):
            x=5+54*s+3*np.sin(2*np.pi*(s*1.2+a)); y=32+k*2+16*np.sin(2*np.pi*(1.3*s-a))*np.sin(np.pi*s)+6*np.sin(2*np.pi*(2.9*s+a))*np.sin(np.pi*s)
            for u,v in zip(x,y): put(f,u,v)
        fr.append(f)
    return fr,95
def discs():
    fr=[];T=12; ys=list(range(54,12,-5))
    for t in range(T):
        f=blank()
        for i,y in enumerate(ys):
            f=ell(f,9,y-6,54,y+6,0,1)
            if (i*T//len(ys))//2==t//2: 
                for x in range(16,48,2): put(f,x,y)
        fr.append(f)
    return fr,120
def axon():
    B=[(0,0,0,16,16,24),(16,0,0,12,16,12),(0,16,0,16,10,8),(16,16,0,12,10,18)]
    def P(X,Y,Z,a,k):
        return 31.5+(X-14)*np.cos(a)-(Y-13)*np.sin(a), 42+((X-14)*np.sin(a)+(Y-13)*np.cos(a))*k-Z
    fr=[]
    for i in range(16):
        u=i/15; a=np.radians(30+30*u); k=.5+.45*u; f=blank()
        for x,y,z,w,d,h in sorted(B,key=lambda b:b[0]+b[1]):
            t=[P(x,y,z+h,a,k),P(x+w,y,z+h,a,k),P(x+w,y+d,z+h,a,k),P(x,y+d,z+h,a,k)]
            l=[P(x,y+d,z+h,a,k),P(x+w,y+d,z+h,a,k),P(x+w,y+d,z,a,k),P(x,y+d,z,a,k)]
            r_=[P(x+w,y,z+h,a,k),P(x+w,y+d,z+h,a,k),P(x+w,y+d,z,a,k),P(x+w,y,z,a,k)]
            f=poly(f,r_,0,1); f=poly(f,l,0,1); f=poly(f,t,0,1)
        fr.append(f)
    return fr+fr[::-1],110
def pixelate():
    u=(xx-31.5)/24;v=(yy-31.5)/24;r2=u*u+v*v;z=np.sqrt(np.clip(1-r2,0,1))
    tone=np.where(r2<1,np.clip(.15+.85*(-.55*u-.55*v+.63*z),0,1),0)
    fr=[]
    for b in (16,8,4,2,1):
        if b==1: fr.append(dith(tone)); continue
        s=ndi.uniform_filter(tone,b,mode='nearest')[b//2::b,b//2::b]
        m=np.kron(s,np.ones((b,b)))[:G,:G]
        fr.append(dith(m) if b<=2 else (m>.42).astype(np.uint8))
    seq=fr+fr[-2:0:-1]; return seq,[500]*len(seq)
def drilled():
    f=blank(); rect(f,8,10,55,53)
    r=rnd(28)
    m=(((xx-31.5)/13)**2+((yy-19)/4.5)**2<1)|((np.abs(xx-31.5)<13)&(yy>19)&(yy<46))|(((xx-31.5)/13)**2+((yy-46)/4.5)**2<1)
    u=np.abs(xx-31.5)/13; s=(r.random((G,G))<(.32+.5*u**2)).astype(np.uint8); f[m]=s[m]
    f=ell(f,18.5,14.5,44.5,23.5,0,1); return f,0
def censored():
    fr=[];W=24;n=6;T=n*W//2
    kinds=[lambda: np.mod(xx,3)==0, lambda: np.mod(xx+yy,4)<2, lambda: None, lambda: np.mod(yy,3)==0, lambda: np.hypot(np.mod(xx,8)-4,np.mod(yy,8)-4)<2, lambda: np.mod(xx-yy,5)<2]
    for t in range(T):
        f=blank(); line(f,0,52,63,52); o=-t*2
        for i in range(-1,n+4):
            x=o+i*W; k=i%n; a=x+3;b=x+20
            if b<0 or a>63: continue
            if k==2:
                for p in range(int(a),int(b)+1,3):
                    put(f,p,20);put(f,p,42)
                for p in range(20,43,3):
                    put(f,a,p);put(f,b,p)
            else:
                m=np.zeros((G,G),bool); m[20:43,max(int(a),0):min(int(b),63)+1]=True; f[m&kinds[k]()]=1; rect(f,a,20,b,42)
        fr.append(f)
    return fr,110
def no_reflect():
    fr=[];T=30
    for t in range(T):
        f=blank(); x=8+47*(.5-.5*np.cos(2*np.pi*t/T)); line(f,0,53,63,53)
        rect(f,5,8,28,48); rect(f,35,8,58,48)
        fill(f,43,28,50,40); fill(f,41,41,52,47)
        figure(f,x,62,1,8)
        if 7<x<27:
            for y in range(30,46):
                if y%2==0: put(f,x,y); put(f,x-1,y)
            fill(f,x-1,26,x,28)
        fr.append(f)
    return fr,100
def statue_droste():
    S=[(-4,-30),(4,-30),(5,-22),(2,-18),(14,-13),(16,14),(11,30),(-11,30),(-16,14),(-14,-13),(-2,-18),(-5,-22)]
    fr=[];T=18;q=.56
    for t in range(T):
        f=blank(); k=t/T*2
        for i in range(-1,9):
            s=1.0*q**(i-k+1)*1.25
            if s<.05: continue
            pts=[(31.5+a*s,30+b*s) for a,b in S]
            f=poly(f,pts,1 if (i%2==0) else 0, 1)
        fr.append(f)
    return fr,110
THIRD=dict(hole_light=hole_light,red_dot=red_dot,slow_cloud=slow_cloud,tunnel=tunnel,spiral_space=spiral_space,peephole=peephole,compartments=compartments,cabinets=cabinets,smoke_stone=smoke_stone,phi=phi,double_sym=double_sym,almost=almost,thin=thin,discs=discs,axon=axon,pixelate=pixelate,drilled=drilled,censored=censored,no_reflect=no_reflect,statue_droste=statue_droste)
if __name__=='__main__':
    import sys
    bad=[]
    for k,fn in THIRD.items():
        if len(sys.argv)>1 and k not in sys.argv[1:]: continue
        try:
            fr,d=fn(); write(k,fr,d)
        except Exception as e:
            import traceback; bad.append((k,traceback.format_exc()[-180:]))
    print(len(THIRD),'bad',bad)
