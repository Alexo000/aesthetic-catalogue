"""Move plates: operations with no catalogue entry, drawn as the move itself. Used only by Actionary's Find one by eye.
They are not observations, so they stay out of the catalogue page. Written to site/moves/."""
import json, os
from plates6 import *
import plates_lib
K=[0,0,0]; W=[244,243,238]
def hold(fr,dur,n,ms):
    return fr,dur
def seq(fr,ms=120,last=2200,first=None):
    d=[ms]*len(fr); d[-1]=last
    if first: d[0]=first
    return fr,d
def bar(f,x0,y0,x1,y1,c=1): fill(f,x0,y0,x1,y1,c); return f

def halve():
    fr=[];x0,x1=4,59
    for i in range(4):
        f=blank(); fill(f,x0,26,x1,37); fr.append(f)
        g=f.copy(); m=(x0+x1)//2; fill(g,m,18,m,45); fr.append(g)
        h=blank(); fill(h,x0,26,m-1,37); fill(h,m+1,26,x1,37,0); dd=dith(np.full((G,G),.25)); mk=(xx>m)&(xx<=x1)&(yy>=26)&(yy<=37); h[mk]=dd[mk]; fr.append(h)
        x1=m-1
    f=blank(); fill(f,x0,26,x1,37); fr.append(f)
    return seq(fr,260,2200)
def ratchet():
    fr=[]
    for n in range(13,-1,-1):
        f=blank(); fill(f,4,58,59,58)
        for i in range(13):
            x=5+i*4
            if i<n: fill(f,x,20,x+2,56)
            else: fill(f,x+1,54,x+1,56)
        fr.append(f)
    return seq(fr,260,2000)
def alternate():
    fr=[];T=2
    for t in range(8):
        f=blank()
        for i in range(8):
            if (i+t)%2==0: fill(f,i*8,8,i*8+7,55)
            else:
                m=(xx>=i*8)&(xx<i*8+8)&(yy>=8)&(yy<=55); f[m]=(((xx+yy)%3==0))[m]
        fr.append(f)
    return fr[:2],520
def saturate():
    fr=[];r=rnd(9);o=r.random((G,G))
    for t in range(16):
        v=(t/15)**1.7*1.15; fr.append((o<v).astype(np.uint8))
    return seq(fr,130,1600)
def sequence():
    H=[10,22,34,46,16,40,28]; order=[4,0,6,2,5,1,3]; fr=[]
    def draw(p):
        f=blank(); fill(f,0,56,63,56)
        for i,k in enumerate(p):
            x=6+i*8; fill(f,x,55-H[k],x+4,55)
        return f
    p=order[:]; fr.append(draw(p))
    for i in range(len(p)):
        for j in range(len(p)-1-i):
            if H[p[j]]>H[p[j+1]]:
                p[j],p[j+1]=p[j+1],p[j]; fr.append(draw(p))
    return seq(fr,240,2200,1000)
def shape(f,k,x,y,r=3):
    if k==0: return ell(f,x-r,y-r,x+r,y+r,1)
    if k==1: fill(f,x-r,y-r,x+r,y+r); return f
    return poly(f,[(x,y-r-1),(x+r+1,y+r),(x-r-1,y+r)],1)
def classify():
    r=rnd(3); N=18; K_=[i%3 for i in range(N)]; A=r.random((N,2))*[52,48]+[6,6]
    B=[]; c=[0,0,0]
    for k in K_:
        B.append((12+k*20,56-c[k]*9)); c[k]+=1
    fr=[]
    for u in list(np.zeros(4))+list(np.linspace(0,1,12)**1.5):
        f=blank(); fill(f,0,61,63,61)
        for k,(a,b),(x,y) in zip(K_,A,B): f=shape(f,k,a+(x-a)*u,b+(y-b)*u)
        fr.append(f)
    return seq(fr,110,2400,120)
def replicate():
    S=path_pts([(8,50),(14,14),(22,40),(28,12)],40); fr=[]
    for i in range(0,len(S)+1,4):
        f=blank(); fill(f,31,4,32,59)
        spread(f,S,1,2); spread(f,[(a+32,b) for a,b in S[:i]],1,2); fr.append(f)
    return seq(fr,90,2200,700)
def interrupt():
    fr=[]; ys=lambda x:C+15*np.sin(x*.32)
    for s in list(range(0,38,3))+[38]*6+list(range(38,64,3)):
        f=blank()
        for x in range(s):
            if x<38 or x>44: fill(f,x,ys(x),x+1,ys(x)+1)
        if 30<=s: fill(f,41,8,41,55)
        fr.append(f)
    return seq(fr,90,1800)
def recall():
    A=[(14,50),(14,20),(32,8),(50,20),(50,50),(32,38)]; n=rnd(6)
    B=[(a+n.integers(-3,4),b+n.integers(-3,4)) for a,b in A]; fr=[];d=[]
    def out(P,k):
        f=blank(); pts=path_pts(P+[P[0]],70)[:k]; spread(f,pts,1,2); return f
    fr.append(out(A,71));d.append(1300)
    fr.append(blank());d.append(900)
    for k in range(5,76,5): fr.append(out(B,k));d.append(80)
    d[-1]=1900
    return fr,d
def roam():
    fr=[];T=20;n=noise3(G,T,2.2,5)
    for t in range(T):
        f=blank(); fill(f,4,30,59,33)
        for k,y0 in enumerate((12,20,44,52)):
            for x in range(4,60):
                y=y0+6*np.sin(x*.16+TAU*t/T+k*1.7)*[1,.8,.8,1][k]
                if (y<28 or y>35) and (k%2==0 or x%2==0): put(f,x,y)
        fr.append(f)
    return fr,120
def reserve():
    fr=[]
    for n in range(0,25,2):
        f=blank()
        for i in range(36):
            x=8+(i%6)*8; y=8+(i//6)*8
            if i<n or i<24 and False: fill(f,x,y,x+5,y+5)
            elif i<24: rect(f,x,y,x+5,y+5) if False else put(f,x+2,y+2)
            else: rect(f,x,y,x+5,y+5)
        fr.append(f)
    return seq(fr,170,2400)
def dissolve():
    m=blank(); fill(m,14,14,49,49); M=m>0
    c=blank(); c=ell(c,12,12,51,51,1); Cc=c>0
    r=rnd(2); A=np.argwhere(M)[::2].astype(float); B=np.argwhere(Cc); B=B[r.permutation(len(B))[:len(A)]].astype(float)
    L=A.copy(); L[:,0]=58-r.random(len(A))*7; L[:,1]=A[:,1]+r.normal(0,5,len(A))
    fr=[];d=[]
    def pts(P):
        f=blank()
        for y,x in P:
            if 0<=int(x)<G and 0<=int(y)<G: f[int(y),int(x)]=1
        return f
    fr.append(np.where(M,1,0).astype(np.uint8));d.append(900)
    for u in np.linspace(0,1,9): fr.append(pts(A+(L-A)*u**1.6));d.append(90)
    d[-1]=800
    for u in np.linspace(0,1,10): fr.append(pts(L+(B-L)*u**.8));d.append(100)
    fr.append(np.where(Cc,1,0).astype(np.uint8));d.append(2000)
    return fr,d
def keystone():
    Bk=[(12,48,27,57),(29,48,44,57),(46,48,57,57) ,(12,37,27,46),(29,37,44,46),(46,37,57,46),(20,26,35,35),(37,26,52,35),(26,15,45,24)]
    def draw(gone,fall=0,kk=None):
        f=blank(); fill(f,0,59,63,59)
        for i,b in enumerate(Bk):
            if i in gone: continue
            dy=0
            if fall and i>=3: dy=min(fall*(1+(i-3)*.4),58-b[3])
            rect(f,b[0],b[1]+dy,b[2],b[3]+dy) if i!=kk else fill(f,b[0],b[1]+dy,b[2],b[3]+dy)
        return f
    fr=[];d=[]
    fr.append(draw(set()));d.append(900)
    fr.append(draw({7}));d.append(600); fr.append(draw(set()));d.append(350)
    fr.append(draw({2}));d.append(600); fr.append(draw(set()));d.append(350)
    fr.append(draw({4}));d.append(320)
    for k in (2,5,9,14,20,26): fr.append(draw({4},k));d.append(80)
    d[-1]=2000
    return fr,d
def join_third():
    fr=[]
    def draw(a,b):
        f=blank(); fill(f,6,24,24,39); fill(f,39,24,57,39)
        fill(f,25-0,a,38,a+6);
        return f
    Y=list(np.linspace(0,28,10))
    for y in Y:
        f=blank(); fill(f,4,24,22,39); fill(f,41,24,59,39)
        m=(xx>=14)&(xx<=49)&(yy>=y)&(yy<=y+6); dd=dith(np.full((G,G),.5)); f[m]=dd[m]; rect(f,14,int(y),49,int(y)+6)
        fr.append(f)
    return seq(fr,120,2200,600)
def exchange():
    fr=[]
    def draw(u):
        f=blank(); fill(f,31,6,32,57) if False else None
        x1=14+36*u; x2=50-36*u; y1=C-9*np.sin(np.pi*u); y2=C+9*np.sin(np.pi*u)
        f=shape(f,0,x1,y1,8); f=shape(f,1,x2,y2,8); return f
    for u in np.r_[np.zeros(3),np.linspace(0,1,10),np.ones(4),np.linspace(1,0,10)]: fr.append(draw(u))
    return fr,110
def hand_over():
    fr=[]
    def draw(ax,bx,ox,oy):
        f=blank(); fill(f,0,56,63,56)
        for x in (ax,bx):
            if x>=3: f=ell(f,x-3,26,x+3,32,1); fill(f,x-3,34,x+3,55)
        fill(f,ox,oy,ox+3,oy+3); return f
    for u in np.linspace(0,1,8): fr.append(draw(20,44,24+14*u,30-8*np.sin(np.pi*u)))
    for u in np.linspace(0,1,10): fr.append(draw(20-20*u,44,38,30))
    return seq(fr,130,2200,900)
def leave_one_out():
    fr=[];o=[3,0,5,1,4,2]
    for k in o+[None]:
        f=blank(); fill(f,0,56,63,56)
        for i in range(6):
            x=7+i*9
            if i==k:
                for y in range(16,56,3): fill(f,x,y,x+3,y) if False else put(f,x+1,y)
            else: fill(f,x,16,x+4,55)
        fr.append(f)
    return seq(fr,520,1500)
def hedge():
    fr=[]
    P=[[(4,32),(22,14),(36,12)],[(4,32),(26,32),(59,32)],[(4,32),(20,50),(32,54)]]
    Q=[path_pts(p,60) for p in P]
    for t in range(2,62,3):
        f=blank()
        for i,q in enumerate(Q):
            spread(f,q[:min(t,len(q))],1,2)
            if i!=1 and t>=len(q): fill(f,q[-1][0]-2,q[-1][1]-2,q[-1][0]+3,q[-1][1]+3,0); rect(f,q[-1][0]-2,q[-1][1]-2,q[-1][0]+3,q[-1][1]+3)
        fr.append(f)
    return seq(fr,90,2200)
def scout():
    fr=[]
    x0=6; xs=[6,8,12,20,36,62]
    for L,ok in ((2,1),(4,1),(8,1),(16,1),(32,1),(50,0)):
        for u in (.4,.8,1):
            f=blank(); fill(f,0,44,4,63);
            fill(f,5,30,5+L*u,33)
            if L==50 and u==1: fill(f,5,30,5+24,33); fill(f,31,34,54,37)
            fill(f,3,20,3,44) if False else None
            fr.append(f)
    return seq(fr,150,2000)
def necker():
    A=[(14,22),(40,22),(40,48),(14,48)]; B=[(24,12),(50,12),(50,38),(24,38)]
    def edges(front,back):
        f=blank()
        for P,dot in ((back,1),(front,0)):
            for a,b in zip(P,P[1:]+P[:1]):
                for s in np.linspace(0,1,40):
                    x=a[0]+(b[0]-a[0])*s;y=a[1]+(b[1]-a[1])*s
                    if not dot or int(s*40)%3: fill(f,x,y,x+1,y+1)
        for a,b in zip(A,B): line(f,a[0],a[1],b[0],b[1])
        return f
    return [edges(A,B),edges(B,A)],[1100,1100]
def layers():
    b=blank(); b=ell(b,18,8,45,35,1); b=poly(b,[(22,32),(41,32),(52,58),(11,58)],1); v=ndi.gaussian_filter(b.astype(float),2.2)*1.0
    fr=[]
    for s in (32,16,8,4,2,1):
        h=v[::s,::s]; o=np.kron(h,np.ones((s,s)))[:G,:G]
        fr.append(dith(np.clip(o,0,1)) if s>1 else b.copy())
    return seq(fr,520,2200)
def load_rest():
    fr=[]; p=[0,.25,.6,1,1,1,.6,.25,0,0,0,0]
    for h in p:
        f=blank(); fill(f,4,8,59,8); fill(f,4,56,59,56); y=52-36*h; fill(f,14,y,49,y+6); fill(f,30,y+6,33,56)
        fr.append(f)
    return fr,[90,90,90,240,240,240,90,90,240,360,360,360]
def plant():
    fr=[]
    for t in range(28):
        f=blank(); fill(f,0,50,63,50)
        fill(f,8,47,10,49);
        x=56-t*1.6
        fill(f,x,38,x+1,49); fill(f,x,35,x+1,36)
        if t>=23:
            r=(t-22)*3; f=ell(f,21-r,48-r,21+r,48+r,1)
        fr.append(f)
    return seq(fr,120,2000)
def pull():
    fr=[];d=[]
    def draw(gone,ref=None):
        f=blank()
        for y in (26,50): fill(f,4,y,59,y)
        for r,y in enumerate((14,38)):
            for c in range(5):
                x=7+c*11;k=r*5+c
                if k in gone: continue
                fill(f,x,y,x+7,y+11)
        return f
    fr.append(draw(set()));d.append(800)
    for k in (7,2,8):
        fr.append(draw({k}));d.append(800)
        fr.append(draw(set()));d.append(650)
    return fr,d
def way_home():
    fr=[]; th=np.linspace(0,TAU,70)
    X=C-24*np.cos(th)*1+0; Y=C-14*np.sin(2*th)
    for t in range(3,71,3):
        f=blank(); f=ell(f,1,26,13,38,1)
        for i in range(0,70,2): put(f,X[i]*0+C-24+48*(i/69 if False else .5)+0 if False else X[i],Y[i])
        spread(f,list(zip(X[:t],Y[:t])),1,2); fr.append(f)
    return seq(fr,90,1800)
def triangulate():
    P=[(3,6),(60,14),(26,60)]; T=(33,27); fr=[]
    for u in np.linspace(.08,1,12):
        f=blank()
        for a,b in P:
            line(f,a,b,a+(T[0]-a)*u,b+(T[1]-b)*u); fill(f,a-1,b-1,a+1,b+1)
        fr.append(f)
    f=fr[-1].copy(); f=ell(f,T[0]-4,T[1]-4,T[0]+4,T[1]+4,1); fr.append(f)
    return seq(fr,110,2200)
def raise_cost():
    fr=[]
    for t in range(6):
        for u in np.linspace(0,1,7):
            f=blank(); fill(f,0,59,63,59)
            for i in range(6):
                h=2+i*i*1.3; fill(f,4+i*10,59-h,11+i*10,59)
            h0=2+(t-1)**2*1.3 if t else 0; h1=2+t*t*1.3
            x=(t*10+7)-10+10*u; y=59-max(h0,0)+(h0-h1)*u-22*np.sin(np.pi*u)
            fill(f,x-1,y-5,x+2,y-1); fr.append(f)
    return fr,[75]*len(fr)
def clear_refill():
    fr=[];d=[]; fieldp=[(xx%2==0),(yy%3==0),((xx+yy)%4==0),(xx%3==0),((xx-yy)%3==0),(yy%2==0)]
    def draw(rest,k):
        f=blank()
        for i in range(6):
            x0=6+(i%3)*18;y0=12+(i//3)*22;m=(xx>=x0)&(xx<x0+16)&(yy>=y0)&(yy<y0+20)
            rect(f,x0,y0,x0+15,y0+19)
            if i==rest: pass
            else: f[m]=fieldp[(i+k)%6][m]; rect(f,x0,y0,x0+15,y0+19)
        return f
    for r,k in ((4,0),(0,1),(5,2),(2,3)):
        fr.append(draw(None,k));d.append(600); fr.append(draw(r,k));d.append(900)
    return fr,d
def delay():
    fr=[]
    for u in np.linspace(0,1,10):
        f=blank(); dd=dith(np.full((G,G),.22)); f[20:]=dd[20:]; fill(f,0,20,63,20)
        y=8+30*u; f=np.array(f); fill(f,26,y,37,y+12,0); rect(f,26,y,37,y+12); fill(f,30,y+5,33,y+7)
        fr.append(f)
    for k in range(10):
        f=fr[9].copy(); fill(f,4,4,4+k*5,6); fr.append(f)
    return seq(fr,150,2000)
def interlock():
    fr=[];C3=[(23,23),(41,23),(32,40)]
    D=[(32,17),(25,33),(39,33)]
    for t in range(9):
        f=blank(); yy2,xx2=yy,xx
        for i,(cx,cy) in enumerate(C3):
            r=np.hypot(xx-cx,yy-cy); w=2 if i==t%3 else 1; f[np.abs(r-17)<(.5*w+.1)]=1
        for x,y in D: fill(f,x-1,y-1,x+1,y+1)
        fr.append(f)
    return fr[:3],700
def share_apart():
    A=(xx%4==0)&(xx>=8)&(xx<=38)&(yy>=8)&(yy<=38)
    B=(yy%4==0)&(xx>=24)&(xx<=55)&(yy>=8)&(yy<=38)
    Cc=((xx+yy)%4==0)&(xx>=16)&(xx<=47)&(yy>=26)&(yy<=55)
    fr=[(A|B|Cc).astype(np.uint8),A.astype(np.uint8),(A|B|Cc).astype(np.uint8),B.astype(np.uint8),(A|B|Cc).astype(np.uint8),Cc.astype(np.uint8)]
    return fr,[1100,700,500,700,500,700]
def breed():
    th=np.linspace(0,TAU,40,endpoint=False); fr=[]; r=rnd(8); amp=np.zeros(5)
    S=[]
    for i in range(5):
        amp=amp+r.normal(0,.7,5)*(1 if i else 0); S.append(amp.copy())
    def dr(f,cx,cy,a,R=8):
        pts=[]
        for t in th:
            q=R+sum(a[k]*np.cos((k+2)*t+k) for k in range(5))*.6; pts.append((cx+q*np.cos(t),cy+q*np.sin(t)))
        return poly(f,pts,1)
    for n in range(1,6):
        f=blank()
        for i in range(n):
            x=10+(i%3)*22; y=18+(i//3)*28; f=dr(f,x,y,S[i])
            if i<n-1 and i!=2: fill(f,x+11,y,x+13,y)
        fr.append(f)
    return seq(fr,600,2200)
def calibrate():
    fr=[]; r=rnd(4); y=C; Y=[]
    for x in range(64):
        y+=.7+.25*r.normal()
        if x%15==14: y=C
        Y.append(y)
    for s in range(2,64,2):
        f=blank()
        for x in range(0,64,3): put(f,x,C-.5)
        for x in (14,29,44,59): fill(f,x,10,x,53)
        for x in range(s): fill(f,x,Y[x],x+1,Y[x]+1)
        fr.append(f)
    return seq(fr,80,1800)
def margin():
    fr=[]; r=rnd(5); P=r.normal(C,16,(14,)); X=np.linspace(6,57,14)
    for u in list(np.zeros(5))+list(np.linspace(0,1,8)):
        f=blank(); fill(f,0,20,63,20); fill(f,0,43,63,43)
        for x,y in zip(X,P):
            t=np.clip(y,23,40); q=y+(t-y)*u; f=ell(f,x-2,q-2,x+2,q+2,1)
        fr.append(f)
    return seq(fr,130,2200,900)
def favour_rare():
    H0=np.array([44,12,28,6,20,36]);H1=np.array([24,24,26,20,24,24]);fr=[]
    for u in np.r_[np.zeros(2),np.linspace(0,1,10)]:
        f=blank(); fill(f,0,56,63,56); h=H0+(H1-H0)*u
        for i,v in enumerate(h): fill(f,5+i*9,55-v,10+i*9,55)
        fr.append(f)
    return seq(fr,130,2200,800)
def archive():
    r=rnd(12); o=r.permutation(36); keep={o[0],o[1],o[2]}; fr=[]
    for n in range(0,34,2):
        f=blank(); gone=set(o[3:3+n])
        for i in range(36):
            x=8+(i%6)*9;y=8+(i//6)*9
            if i in keep: fill(f,x-1,y-1,x+5,y+5)
            elif i not in gone: rect(f,x,y,x+4,y+4)
        fr.append(f)
    return seq(fr,150,2400,800)
def cut_beaten():
    r=rnd(21); P=r.random((26,2))*[50,50]+[7,7]
    front=[i for i,p in enumerate(P) if not any((q[0]>p[0] and q[1]>p[1]) for q in P)]
    rest=[i for i in range(26) if i not in front]; fr=[]
    for n in range(0,len(rest)+1,2):
        f=blank(); fill(f,4,4,4,59); fill(f,4,59,59,59)
        for i,p in enumerate(P):
            if i in rest[:n]: continue
            x,y=p[0],63-p[1]
            f=ell(f,x-2,y-2,x+2,y+2,1) if i in front else ell(f,x-1,y-1,x+1,y+1,0,1)
        fr.append(f)
    return seq(fr,190,2400,800)
def no_winner():
    Pt=[(32,12),(53,46),(11,46)]; fr=[]
    for k in range(3):
        for u in np.linspace(.15,.8,8):
            f=blank()
            for i,(x,y) in enumerate(Pt):
                f=ell(f,x-6,y-6,x+6,y+6,1) if i==k else ell(f,x-6,y-6,x+6,y+6,0,1)
            for i in range(3):
                a,b=Pt[i],Pt[(i+1)%3]
                for s in np.linspace(.22,.78,18):
                    if int(s*30)%2: put(f,a[0]+(b[0]-a[0])*s,a[1]+(b[1]-a[1])*s)
            a,b=Pt[k],Pt[(k+1)%3]; fill(f,a[0]+(b[0]-a[0])*u-1,a[1]+(b[1]-a[1])*u-1,a[0]+(b[0]-a[0])*u+1,a[1]+(b[1]-a[1])*u+1)
            fr.append(f)
    return fr,100
def suspend():
    r=rnd(3); ring=np.abs(np.hypot(xx-C,yy-C)-20)<.8; fr=[];T=16
    ph=r.random((9,9,2))*TAU
    for t in range(T):
        f=blank(); f[ring]=1
        for i in range(9):
            for j in range(9):
                x=4+i*7.0;y=4+j*7.0
                if np.hypot(x-C,y-C)<18:
                    x+=5*np.cos(TAU*t/T+ph[i,j,0])*1.1;y+=5*np.sin(TAU*t/T*1+ph[i,j,1])
                    fill(f,x,y,x+1,y+1)
                elif np.hypot(x-C,y-C)>22:
                    y=(y+t*7/T*1)
                    y=y if y<63 else y-63
                    fill(f,x,y,x+1,y+1)
        fr.append(f)
    return fr,120
def oddities():
    fr=[];T=24
    for t in range(T):
        f=blank(); fill(f,0,44,63,44); fill(f,0,47,63,47)
        for i in range(-1,5):
            x=(i*16+t*16/6.0)%96-16
            odd=(i==1)
            if odd: f=poly(f,[(x+6,28),(x+12,42),(x,42)],1)
            else: fill(f,x+1,31,x+11,42) if not odd else None
        fr.append(f)
    return fr,110
def braided():
    fr=[];T=18
    for t in range(T):
        f=blank(); fill(f,0,4,63,5); fill(f,0,58,63,59)
        for k,(a,p) in enumerate(((20,0),(20,2.1),(20,4.2),(12,1.1),(12,3.3))):
            for x in range(64):
                y=C+a*np.sin(x*.1+p+TAU*t/T)*.92+ (k-2)*1.3
                put(f,x,y);
        fr.append(f)
    return fr,120
def stitch():
    n=noise2(G,3.2,30); sc=(n+ (yy-40)/34>.2)
    fr=[]
    for k in range(1,5):
        for o in (12,6,0):
            f=blank()
            for i in range(k):
                w=i*14+4; dx=o if i==k-1 else 0; dy=(-1)**i*3 if i==k-1 and o else 0
                m=(xx>=w+dx)&(xx<w+16+dx)&(yy>=14+dy)&(yy<50+dy)
                sh=np.roll(sc,0)
                f[m]=sh[m]; rect(f,w+dx,14+dy,w+15+dx,49+dy) if o else None
            fr.append(f)
    return seq(fr,170,2200)

M=dict(halve=halve,ratchet=ratchet,alternate=alternate,saturate=saturate,sequence=sequence,classify=classify,replicate=replicate,interrupt=interrupt,
 recall=recall,roam=roam,reserve=reserve,dissolve_and_rebuild=dissolve,find_the_keystone=keystone,join_through_a_third=join_third,exchange=exchange,hand_over=hand_over,
 leave_one_out=leave_one_out,hedge=hedge,scout=scout,leave_open=necker,build_in_layers=layers,load_and_rest=load_rest,plant=plant,pull=pull,keep_a_way_home=way_home,
 triangulate=triangulate,raise_the_cost=raise_cost,clear_and_refill=clear_refill,delay=delay,interlock=interlock,share_and_keep_apart=share_apart,breed=breed,
 calibrate=calibrate,allow_a_margin=margin,favour_the_rare=favour_rare,archive=archive,cut_the_beaten=cut_beaten,leave_no_winner=no_winner,suspend_the_rules=suspend,
 feed_in_oddities=oddities,watch_for_clashes=braided)
if __name__=='__main__':
    import sys,traceback
    plates_lib.OUT='site/moves'; os.makedirs('site/moves',exist_ok=True)
    for k,fn in M.items():
        if len(sys.argv)>1 and k not in sys.argv[1:]: continue
        try:
            o=fn(); write(k,o[0],o[1]); print(k,len(o[0]))
        except Exception:
            print('FAIL',k,traceback.format_exc()[-260:])
