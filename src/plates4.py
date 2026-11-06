"""Plates chosen for effects and viewpoints the catalogue did not have, then a set on colour. Same 64 by 64 grid."""
from plates3 import *
C=31.5
def ease(u): return u*u*(3-2*u)
# looking up or down
def depth():
    fr=[];T=14
    for t in range(T):
        q=.62+.25*ease(t/(T-1)); f=blank()
        for a,b in ((0,0),(63,0),(0,63),(63,63)): line(f,a,b,C+(a-C)*.06,C+(b-C)*.06)
        for i in range(0,16):
            r=31*q**i
            if r>1: rect(f,C-r,C-r,C+r,C+r)
        fr.append(f)
    return fr+fr[::-1],95
def heights():
    # looking straight up between four towers; the head sways, so the vanishing point drifts
    fr=[];T=20
    for t in range(T):
        a=2*np.pi*t/T;vx=C+4*np.cos(a);vy=C+4*np.sin(a);f=np.ones((G,G),np.uint8)
        Q=[((-1,-1),(9,-1),(-1,9)),((65,-1),(55,-1),(65,9)),((-1,65),(-1,55),(9,65)),((65,65),(65,55),(55,65))]
        Q=[[(-1,-1),(22,-1),(vx-1.5,vy-1.5),(-1,22)],[(65,-1),(42,-1),(vx+1.5,vy-1.5),(65,22)],[(-1,65),(22,65),(vx-1.5,vy+1.5),(-1,42)],[(65,65),(42,65),(vx+1.5,vy+1.5),(65,42)]]
        for q in Q: f=poly(f,q,0)
        for ex,ey in ((-1,8),(-1,16),(8,-1),(16,-1),(65,8),(65,16),(48,-1),(56,-1),(-1,48),(-1,56),(8,65),(16,65),(48,65),(56,65),(65,48),(65,56)):
            line(f,ex,ey,vx,vy)
        fr.append(f)
    return fr,100
def overhead():
    r=rnd(31);N=16;x=r.integers(8,56,N).astype(float);y=r.integers(8,56,N).astype(float);v=r.choice([-1,1],N);h=r.choice([0,1],N);fr=[]
    for t in range(48):
        f=blank()
        for a in range(10,56,8):
            for b in range(10,56,8): put(f,a,b)
        rect(f,5,5,58,58); rect(f,3,3,60,60)
        for i in range(N):
            d=v[i]*t*1.0
            X=8+((x[i]-8+(d if h[i] else 0))%48); Y=8+((y[i]-8+(0 if h[i] else d))%48)
            fill(f,X,Y,X+1,Y+1); put(f,X+2,Y+2)
        fr.append(f)
    return fr,100
def underground():
    b=stip(.1,41); b=np.array(b); r=rnd(42)
    for y in (6,28,46): b[y:y+2]=(r.random((2,G))<.6)
    def cube(x,y,s):
        nonlocal b
        b=poly(b,[(x,y),(x+s,y-s//2),(x+2*s,y),(x+s,y+s//2)],0,1)
        b=poly(b,[(x,y),(x+s,y+s//2),(x+s,y+s+s//2),(x,y+s)],0,1)
        b=poly(b,[(x+2*s,y),(x+s,y+s//2),(x+s,y+s+s//2),(x+2*s,y+s)],0,1)
    cube(8,16,9);cube(36,36,12);cube(42,8,6)
    return [np.roll(b,-2*t,0) for t in range(32)],100
# moving past or through
def doorway():
    fr=[];T=22
    for t in range(T):
        u=ease(t/(T-1));s=.32+.95*u; f=blank()
        w=20*s;h=40*s;y1=C+24*s; 
        for a,b in ((0,63),(63,63)): line(f,a,b,C+(a-C)*.2,y1)
        o=np.zeros((G,G),np.uint8); o[max(int(y1-h),0):min(int(y1),63)+1,max(int(C-w),0):min(int(C+w),63)+1]=1
        k=s**1.7
        o=ell(o,C-7*k,y1-24*k-h*.02,C+7*k,y1-10*k,0); fill(o,C-3*k,y1-11*k,C+3*k,y1,0)
        f=np.maximum(f,o); fr.append(f)
    return fr,[90]*(T-1)+[900]
def gallery_angle():
    fr=[];n=16
    for i in range(n):
        a=np.radians(-72+144*i/(n-1));f=blank();line(f,0,54,63,54)
        for u in np.linspace(-.5,.5,120):
            d=1+u*np.sin(a)*1.1; x=C+u*44*np.cos(a)/d
            for v in np.linspace(-.5,.5,90):
                y=30+v*38/d
                e=max(abs(u),abs(v))>.47; ring=abs(np.hypot(u,v)-.3)<.04; dot=np.hypot(u,v)<.08
                if e or ring or dot: put(f,x,y)
        fr.append(f)
    return fr+fr[::-1],100
def scroll():
    fr=[]; X=np.arange(128)
    h=30+7*np.sin(2*np.pi*X/128*3)+4*np.sin(2*np.pi*X/128*7+1)+2*np.sin(2*np.pi*X/128*13)
    h2=40+5*np.sin(2*np.pi*X/128*5+2)+3*np.sin(2*np.pi*X/128*11)
    for t in range(64):
        f=blank()
        for x in range(9,55):
            k=(x+2*t)%128
            put(f,x,h[k]); put(f,x,h2[k])
            for y in range(int(h2[k]),46,2):
                if (x+y)%3==0: put(f,x,y)
        rect(f,9,18,54,46)
        for x in (3,55):
            fill(f,x,14,x+5,50); 
            for y in range(16,49,3): line(f,x+1,y,x+4,y,0)
        fr.append(f)
    return fr,100
def candles():
    fr=[];T=9;q=.7;r=rnd(32)
    for t in range(T):
        f=blank(); line(f,0,63,C-2,34); line(f,63,63,C+2,34); line(f,0,0,C-2,30); line(f,63,0,C+2,30)
        for i in range(0,9):
            s=q**(i+1-t/T)
            for sg in (-1,1):
                x=C+sg*40*s; y=34+24*s; h=max(1,round(14*s)); w=max(0,round(1.6*s))
                if x-w<0 or x+w>63: continue
                fill(f,x-w,y-h,x+w,y); fh=max(1,round(6*s*(.7+.5*r.random()))); fill(f,x-max(w-1,0),y-h-fh-1,x+max(w-1,0),y-h-2)
        fr.append(f)
    return fr,110
# seeing two things at once
def mirror45():
    fr=[];T=20
    for t in range(T):
        a=np.pi/2*t/T;f=blank(); f=poly(f,[(12,4),(52,4),(58,26),(6,26)],0,1)
        c,s=np.cos(a),np.sin(a); P=[(C+(u*c-v*s)*1.0,15+(u*s+v*c)*.72) for u,v in ((-9,-9),(9,-9),(9,9),(-9,9))]
        f=poly(f,P,1); xs=[C+(u*c-v*s) for u,v in ((-9,-9),(9,-9),(9,9),(-9,9))]
        line(f,0,56,63,56); x0,x1=min(xs),max(xs); e=sorted(xs)
        f=poly(f,[(x0,34),(x1,34),(x1,55),(x0,55)],0,1); line(f,e[1],34,e[1],55); line(f,e[2],34,e[2],55)
        fr.append(f)
    return fr,110
def prisms_view():
    fr=[];T=20
    for t in range(T):
        k=.5-.5*np.cos(2*np.pi*t/T); a=2*np.pi*t/T/3; f=np.zeros((G,G),bool)
        for i in range(6):
            b=a+i*np.pi/3; m=np.hypot(xx-C-17*k*np.cos(b),yy-C-17*k*np.sin(b))<9; f^=m
        fr.append(f.astype(np.uint8))
    return fr,120
def rot_mirror():
    fr=[];T=24
    src=blank(); figure(src,C,46,1,26); src=ell(src,44,10,52,18,1); line(src,8,46,55,46)
    for t in range(T):
        a=2*np.pi*t/T;c=np.cos(a);f=blank();w=max(abs(c),.04)
        m=((xx-C)/(26*w))**2+((yy-C)/26)**2<1
        if c>0:
            sx=np.clip(C+(xx-C)/w,0,63).astype(int); f[m]=src[yy,sx][m]
        else:
            sx=np.clip(C-(xx-C)/w,0,63).astype(int); f[m]=dith(np.full((G,G),.25))[m]*0+src[yy,sx][m]
        o=(((xx-C)/(26*w+1))**2+((yy-C)/27)**2<1)&~m; f[o]=1; fr.append(f.astype(np.uint8))
    return fr,95
def ball_lens():
    fr=[];T=14;R=25;u=(xx-C)/R;v=(yy-C)/R;r=np.hypot(u,v);m=r<1;th=np.arctan2(v,u);rr=np.tan(np.clip(r,0,.97)*1.25)*1.2
    X=rr*np.cos(th);Y=rr*np.sin(th)
    for t in range(T):
        c=(np.floor((X+t/T*2)*3)+np.floor(Y*3))%2
        f=((c>0)&m).astype(np.uint8); o=(r<1.14)&~m; f[o]=1; fr.append(f)
    return fr,110
def painting_zoom():
    n=14;fr=[];cx,cy=44.,41.
    M=[(4,44),(14,28),(22,36),(32,16),(44,34),(52,26),(60,44)]
    for i in range(n):
        s=1+7*ease(i/(n-1));f=blank()
        T=lambda x,y:(C+(x-cx)*s,C+(y-cy)*s)
        def L(a,b):
            p=T(*a);q=T(*b)
            if max(abs(p[0]),abs(q[0]),abs(p[1]),abs(q[1]))<400: line(f,*p,*q)
        for a,b in zip(M,M[1:]): L(a,b)
        L((2,48),(61,48)); L((8,54),(24,50)); L((30,58),(56,52))
        for a,b in (((42,42),(46,42)),((46,42),(46,45)),((42,45),(46,45)),((42,42),(42,45)),((41,42),(44,39.5)),((44,39.5),(47,42))): L(a,b)
        L((44,45),(44,43.8))
        p=T(47.6,44.4); fill(f,p[0],p[1]-max(1,.9*s),p[0]+max(0,.3*s),p[1]+max(0,.6*s))
        if s<1.6: rect(f,1,1,62,62)
        fr.append(f)
    return fr+fr[::-1],[120]*n+[700]+[120]*(n-1)
# effects on the image
def heat():
    fr=[];T=10
    base=((np.mod(yy,8)==0)|(np.mod(xx+((yy//8)%2)*6,12)==0))
    for t in range(T):
        ph=2*np.pi*t/T; A=np.clip((46-np.abs(xx-C)*.6-(yy-6)*.3)/10,0,1)*np.clip((48-yy)/10,0,1)*3.4
        dx=(A*np.sin(yy*.55-ph)).astype(int); sx=np.clip(xx+dx,0,63)
        f=base[yy,sx].astype(np.uint8)
        f=ell(f,16,44,47,75,0,1); fill(f,0,60,63,63,1)
        s=dith(np.clip((yy-48)/14,0,.9)*np.exp(-np.abs(xx-C)/14)); m=((xx-C)/14)**2+((yy-60)/14)**2<1; f[m]=s[m]; fr.append(f)
    return fr,90
def film_mirror():
    src=blank(); figure(src,C,54,1,30); rect(src,6,4,57,59)
    for y in range(10,56,9):
        for x in range(8,56,2): put(src,x,y)
    fr=[];dur=[]
    r=np.hypot(xx-22,yy-24)+.01
    for t in range(14):
        A=7*.8**t; w=np.sin(r*.9-t*1.2)*A*np.exp(-r/28)
        sx=np.clip((xx+w*(xx-22)/r).astype(int),0,63); sy=np.clip((yy+w*(yy-24)/r).astype(int),0,63); fr.append(src[sy,sx]);dur.append(75)
    fr.append(src);dur.append(1500); return fr,dur
GL={'L':'10000 10000 10000 10000 10000 10000 11111','I':'111 010 010 010 010 010 111','G':'01110 10001 10000 10111 10001 10001 01110','H':'10001 10001 10001 11111 10001 10001 10001','T':'11111 00100 00100 00100 00100 00100 00100'}
def letters():
    t0=blank();x=11
    for ch in 'LIGHT':
        for j,row in enumerate(GL[ch].split()):
            for i,c in enumerate(row):
                if c=='1': fill(t0,x+i*1,14+j*2,x+i*1,15+j*2)
        x+=len(GL[ch].split()[0])+3
    fr=[];T=12
    for t in range(T):
        f=np.array(t0); line(f,0,31,63,31)
        for y in range(32,60):
            d=int(np.sin(y*.7-2*np.pi*t/T)*(y-30)*.12); src=30-(y-31)
            if src>=0 and y%3!=2: f[y]=np.roll(t0[src],d)
        fr.append(f)
    return fr,100
def pendulum():
    th1,th2,w1,w2=2.5,2.2,0.,0.;dt=.02;P=[];L=14.
    for i in range(44):
        for k in range(9):
            a1=-3*np.sin(th1)-np.sin(th1-2*th2)-2*np.sin(th1-th2)*(w2*w2+w1*w1*np.cos(th1-th2))
            a1/=(3-np.cos(2*th1-2*th2))
            a2=2*np.sin(th1-th2)*(2*w1*w1+2*np.cos(th1)+w2*w2*np.cos(th1-th2))/(3-np.cos(2*th1-2*th2))
            w1+=a1*dt*9.8/4;w2+=a2*dt*9.8/4;th1+=w1*dt;th2+=w2*dt
        x1=C+L*np.sin(th1);y1=26+L*np.cos(th1);x2=x1+L*np.sin(th2);y2=y1+L*np.cos(th2);P.append((x1,y1,x2,y2))
    fr=[]
    for i in range(44):
        f=blank();fill(f,C-1,25,C+1,27)
        for j in range(max(0,i-4),i+1):
            x1,y1,x2,y2=P[j];line(f,C,26,x1,y1);line(f,x1,y1,x2,y2);fill(f,x2-1,y2-1,x2,y2)
        fr.append(f)
    return fr,[320 if i%1==0 else 0 for i in range(44)]
def timelapse():
    fr=[];n=30;e=noise2(G,1.4,51)
    for i in range(n):
        f=blank();line(f,0,56,63,56);g=min(i/10,1);top=54-int(38*g)
        fill(f,18,top,44,55)
        for y in range(top+2,54,4):
            for x in range(21,43,5): fill(f,x,y,x+1,y+1,0)
        k=max(0,(i-13)/(n-14)); th=1.8-3.8*k
        if k>0: f[(e<th)==False]=0; line(f,0,56,63,56)
        a=(i*2.2)%1; x=4+a*56;y=10-8*np.sin(np.pi*a); fill(f,x,y,x+1,y+1); fr.append(f)
    return fr,[170]*(n-1)+[900]
def drips():
    r=rnd(52);L=ndi.gaussian_filter1d(r.random(G)**3,1.3,mode='wrap');L=L/L.max();fr=[];T=18
    for t in range(T):
        f=blank();k=t/(T-1);f[:10,:]=1
        for x in range(G):
            f[10:int(10+L[x]*50*k+3*k)+0,x]=1
        fr.append(f)
    return fr,[190]*(T-1)+[1600]
def fridge():
    n=noise2(G,2.0,53);fr=[];w=ndi.gaussian_filter(n,1.5)
    for t in range(16):
        f=blank();s=np.roll(w,4*t,0);v=np.clip((yy-10)/40,0,1)*0+.62
        spread=np.abs(xx-C)<14+np.clip(yy-34,0,30)*.7
        floor=np.clip((yy-46)/16,0,1)
        q=(v+.28*s)*spread*np.clip(1.15-yy/110,0,1)*(1+.35*floor)
        q[:10]=0; f=dith(np.clip(q-.1,0,1)); f=np.array(f)
        rect(f,16,1,47,16); line(f,16,6,47,6); line(f,16,11,47,11); fr.append(f)
    return fr,110
def odd_clock():
    A=[0,30,60,150,160,170,260,270,360];D=[160,160,900,110,110,800,110,1500];fr=[]
    for a in A[:-1]:
        f=blank();f=ell(f,6,6,57,57,0,1)
        for i in range(12):
            b=np.radians(i*30);put(f,C+22*np.sin(b),C-22*np.cos(b))
        b=np.radians(a);line(f,C,C,C+19*np.sin(b),C-19*np.cos(b));fill(f,C-1,C-1,C+1,C+1);fr.append(f)
    return fr,D
# invisible things and form
def force():
    fr=[];T=10;R2=170.
    for t in range(T):
        f=blank()
        for y0 in range(-27,28,6):
            y0=y0+.5
            for x in np.arange(-34+t*1.2,36,6):
                k=1+R2/(x*x+y0*y0+R2*.35); fill(f,C+x,C+y0*k,C+x+1,C+y0*k)
        fr.append(f)
    return fr,95
def watcher():
    def m(d):
        f=blank();f=ell(f,20,6,43,36,0,1);f=poly(f,[(4,63),(10,46),(24,40),(40,40),(54,46),(60,63)],0,1);f=ell(f,20,6,43,36,0,1)
        f=poly(f,[(26,41),(32,47),(38,41)],1)
        f=ell(f,24,19,29,23,0,1);f=ell(f,35,19,40,23,0,1);fill(f,26+d,20,27+d,22);fill(f,37+d,20,38+d,22);line(f,31,25,30,30);line(f,30,30,33,30);line(f,27,33,36,33);return f
    return [m(0),m(-1),m(0),m(1)],[1800,800,500,900]
def torus():
    fr=[];T=14;ti=.75;c_,s_=np.cos(ti),np.sin(ti)
    for t in range(T):
        f=blank();ph=(2*np.pi/12)*t/T
        for i in range(12):
            u=ph+i*2*np.pi/12
            for v in np.linspace(0,2*np.pi,70):
                r=19+8*np.cos(v);x,y,z=r*np.cos(u),r*np.sin(u),8*np.sin(v);Y=y*c_-z*s_;Z=y*s_+z*c_
                if Z>-11 or abs(v-np.pi)>1: put(f,C+x,C+Y)
        for v0 in (0,np.pi/2,-np.pi/2):
            for u in np.linspace(0,2*np.pi,160):
                r=19+8*np.cos(v0);x,y,z=r*np.cos(u),r*np.sin(u),8*np.sin(v0);put(f,C+x,C+(y*c_-z*s_))
        fr.append(f)
    return fr,100
def no_ends():
    fr=[];T=12;s=np.linspace(0,2*np.pi,520,endpoint=False)
    x=C+26*np.sin(s);y=C+15*np.sin(2*s)
    for t in range(T):
        f=blank()
        for i,(a,b) in enumerate(zip(x,y)):
            if (i/520*20-t/T)%1<.62: fill(f,a,b,a+1,b+1)
        fr.append(f)
    return fr,95
def rot_wall():
    fr=[];T=14
    def d(a):
        f=blank();rect(f,6,14,57,49);line(f,C,14,C,49,0) if False else None
        fill(f,C,14,C,14,0)
        L=17.5;line(f,C,C,C+L*np.cos(a),C+L*np.sin(a));line(f,C,C,C-L*np.cos(a),C-L*np.sin(a));line(f,C+1,C,C+1+L*np.cos(a),C+L*np.sin(a));line(f,C+1,C,C+1-L*np.cos(a),C-L*np.sin(a));fill(f,C-1,C-1,C+2,C+2);return f
    S=[d(np.pi/2*ease(i/(T-1))) for i in range(T)]
    fr=S+S[::-1]; return fr,[100]*(T-1)+[1100]+[100]*(T-1)+[1100]

# colour, each plate with its own small palette
def neon_orange():
    P=[0,0,0, 7,11,64, 3,5,30, 255,98,0]
    v=(yy/G);b=dith(np.clip(.2+.75*(1-v),0,1));g=np.where(b>0,1,2).astype(np.uint8);g[:]=np.where(np.abs(yy-32)>22,0,g)
    on=np.array(g);on=ell(on,14,10,49,45,None,3);on=ell(on,15,11,48,44,None,3);on=np.array(on);fill(on,31,45,32,56,3)
    off=np.array(g);
    return ([on,off,on,off,on],[1500,70,120,60,2300],P)
def fuchsia():
    P=[2,4,28, 8,14,84, 255,0,170];fr=[];T=16
    for t in range(T):
        a=2*np.pi*t/T;f=dith(np.clip(.35+.5*np.sin(xx*.09+yy*.06),0,1))
        for i in range(3):
            b=a+i*2*np.pi/3;x=C+15*np.cos(b);y=C+15*np.sin(b);m=np.abs(np.hypot(xx-x,yy-y)-11)<1.6;f=np.array(f);f[m]=2
        fr.append(f)
    return (fr,110,P)
def blue_green():
    P=[0,0,0, 0,222,186];fr=[];T=16;r=np.hypot(xx-C,(yy-20)*.8)
    w=np.abs(xx-C)-(6+.42*yy)
    for t in range(T):
        k=.5-.5*np.cos(2*np.pi*t/T);v=np.clip(-w/18,0,1)*(.45+.45*k)*np.clip(1.1-yy/80,0,1);f=dith(v);fr.append(f)
    return (fr,150,P)
def red_faint():
    P=[255,255,255, 255,246,245, 254,240,239];r=np.hypot(xx-C,yy-C);f=np.zeros((G,G),np.uint8);f[r<25]=1;f[(r<25)&(np.mod(xx+yy,4)==0)]=2;f[r<10]=2
    return (f,0,P)
def yellow_black():
    P=[0,0,0, 255,228,0];fr=[];T=12;r=np.hypot(xx-C,yy-C);a=np.arctan2(yy-C,xx-C)
    for t in range(T):
        f=(np.sin(r*.8-a*3+2*np.pi*t/T)>-.45).astype(np.uint8);fr.append(f)
    return (fr,95,P)
def red_green():
    P=[52,104,80, 214,22,48, 22,44,36];fr=[];T=20
    for t in range(T):
        a=2*np.pi*t/T;A=np.mod(xx*.9+7*np.sin(yy*.09+a),3)<1.5;B=np.mod(xx*1.0+yy*.1,3)<1.5
        f=np.where(A^B,1,0).astype(np.uint8);f[(yy+xx)%6==0]=np.where(f[(yy+xx)%6==0]==0,2,1);fr.append(f)
    return (fr,110,P)
def golds():
    P=[255,224,44, 226,172,40, 178,128,30, 122,84,22, 64,42,14, 22,14,6];fr=[];T=14
    for t in range(T):
        g=-14+92*t/(T-1);f=np.zeros((G,G),np.uint8)
        for i in range(6):
            x=i*10+2;m=(xx>=x)&(xx<x+10);d=dith(np.full((G,G),.5));sh=np.abs(xx+yy*.4-g)<6;v=np.clip(i-(sh*2),0,5)
            f[m]=(v+(d*(i<5)*(~sh)))[m]
        f[:6,:]=5;f[58:,:]=5;fr.append(f.astype(np.uint8))
    return (fr,110,P)
def lips():
    P=[0,0,0, 232,0,34, 255,255,255];fr=[];T=12
    for t in range(T):
        k=.5-.5*np.cos(2*np.pi*t/T);f=blank();gap=1+2*k
        f=poly(f,[(10,31),(21,22),(29,24),(32,26),(35,24),(43,22),(54,31),(43,32-gap+1),(21,32-gap+1)],1)
        f=poly(f,[(10,32),(21,32+gap),(43,32+gap),(54,32),(44,42),(32,45),(20,42)],1)
        x=22+18*k;f=ell(f,x,35+gap,x+6,38+gap,2);fr.append(f)
    return (fr,120,P)
def neon_words():
    # GAS read backwards is SAG, and the word sags. Neon burns red-orange, argon blue.
    L={'G':[(10,2),(2,2),(0,4),(0,14),(2,16),(10,16),(10,9),(6,9)],'A':[(0,16),(5,0),(10,16)],'A2':[(2,10),(8,10)],'S':[(10,2),(2,2),(0,4),(0,7),(2,9),(8,9),(10,11),(10,14),(8,16),(0,16)]}
    def word(w,oy,sag,c):
        f=blank();x0=7
        for ch in w:
            for k in ([ch,'A2'] if ch=='A' else [ch]):
                P=L[k]
                for (a,b),(d,e) in zip(P,P[1:]):
                    for u in np.linspace(0,1,40):
                        x=x0+(a+(d-a)*u)*1.3; y=oy+(b+(e-b)*u)+sag*np.sin(np.pi*x/63)
                        fill(f,x,y,x+1,y+1,1)
            x0+=18
        d=ndi.distance_transform_edt(f==0);h=dith(np.exp(-d/2.6)*.5)
        o=blank();o[h>0]=c+2;o[f>0]=c;return o
    a=word('GAS',5,0,1);b=word('SAG',33,9,2);z=blank()
    return ([a,z,a,z,b,z,b,z],[1100,70,120,260,1100,70,120,260],[0,0,0, 255,72,30, 96,126,255, 112,30,12, 34,44,110])
FOURTH=dict(depth=depth,heights=heights,overhead=overhead,underground=underground,doorway=doorway,gallery_angle=gallery_angle,scroll=scroll,candles=candles,mirror45=mirror45,prisms_view=prisms_view,rot_mirror=rot_mirror,ball_lens=ball_lens,painting_zoom=painting_zoom,heat=heat,film_mirror=film_mirror,letters=letters,pendulum=pendulum,timelapse=timelapse,drips=drips,fridge=fridge,odd_clock=odd_clock,force=force,watcher=watcher,torus=torus,no_ends=no_ends,rot_wall=rot_wall,red_faint=red_faint)
if __name__=='__main__':
    import sys,traceback
    bad=[]
    for k,fn in FOURTH.items():
        if len(sys.argv)>1 and k not in sys.argv[1:]: continue
        try:
            o=fn(); write(k,o[0],o[1],o[2] if len(o)>2 else None)
        except Exception:
            bad.append((k,traceback.format_exc()[-200:]))
    print(len(FOURTH),'bad',bad)
