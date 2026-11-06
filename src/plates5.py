"""The colour plates. Black and white first; colour is a small, soft accent, so these sit among the rest."""
from plates4 import *
K=[0,0,0]; W=[244,243,238]
EMBER=[206,92,62]; ARGON=[122,140,206]; ROSE=[196,84,146]; TEAL=[104,180,164]; PALE=[226,204,110]; RED=[190,58,52]; LEAF=[92,124,104]; INK=[22,30,86]
def red_light():
    r=np.hypot(xx-C,yy-C); f=dith(np.clip(1-r/25,0,1)**1.8*.7); return (f,0,K+RED)
def neon_words():
    L={'G':[(10,2),(2,2),(0,4),(0,14),(2,16),(10,16),(10,9),(6,9)],'A':[(0,16),(5,0),(10,16)],'A2':[(2,10),(8,10)],'S':[(10,2),(2,2),(0,4),(0,7),(2,9),(8,9),(10,11),(10,14),(8,16),(0,16)]}
    def word(w,oy,sag,c):
        f=blank();x0=7
        for ch in w:
            for k in ([ch,'A2'] if ch=='A' else [ch]):
                P=L[k]
                for (a,b),(d,e) in zip(P,P[1:]):
                    for u in np.linspace(0,1,40):
                        x=x0+(a+(d-a)*u)*1.3; y=oy+(b+(e-b)*u)+sag*np.sin(np.pi*x/63); put(f,x,y); put(f,x+1,y)
            x0+=18
        d=ndi.distance_transform_edt(f==0);h=dith(np.exp(-d/2.2)*.34)
        o=blank();o[h>0]=c;o[f>0]=1;return o
    a=word('GAS',5,0,2);b=word('SAG',33,9,3);z=blank()
    return ([a,z,a,z,b,z,b,z],[1100,70,120,260,1100,70,120,260],K+W+EMBER+ARGON)
def neon_orange():
    bg=(stip(.05,61)*3).astype(np.uint8)
    t=blank();t=ell(t,15,11,48,44,None,1);fill(t,31,45,31,56);d=ndi.distance_transform_edt(t==0);h=dith(np.exp(-d/2.4)*.32)
    on=np.array(bg);on[h>0]=2;on[t>0]=1
    return ([on,bg,on,bg,on],[1500,70,120,60,2300],K+W+EMBER+INK)
def fuchsia():
    fr=[];T=16;bg=(stip(.07,62)*3).astype(np.uint8)
    for t in range(T):
        a=2*np.pi*t/T;f=np.array(bg)
        for i in range(3):
            b=a+i*2*np.pi/3;x=C+15*np.cos(b);y=C+15*np.sin(b);m=np.abs(np.hypot(xx-x,yy-y)-11)<(.9 if i else 1.1);f[m]=2 if i==0 else 1
        fr.append(f)
    return (fr,110,K+W+ROSE+INK)
def blue_green():
    fr=[];T=16;w=np.abs(xx-C)-(5+.36*yy)
    for t in range(T):
        k=.5-.5*np.cos(2*np.pi*t/T);v=np.clip(-w/20,0,1)*(.2+.28*k)*np.clip(1.1-yy/80,0,1);f=dith(v)*2;f=np.array(f,np.uint8);fill(f,28,0,35,3,1);fr.append(f)
    return (fr,150,K+W+TEAL)
def yellow_black():
    fr=[];T=18;base=(np.mod(np.maximum(np.abs(xx-C),np.abs(yy-C)),4)<1.5).astype(np.uint8)
    for t in range(T):
        a=2*np.pi*t/T;x=C+17*np.cos(a);y=C+17*np.sin(a);m=(np.abs(xx-x)<7)&(np.abs(yy-y)<7);f=np.array(base);f[m&(base>0)]=2;fr.append(f)
    return (fr,110,K+W+PALE)
def red_green():
    fr=[];T=20
    for t in range(T):
        a=2*np.pi*t/T;A=np.mod(xx+5*np.sin(yy*.1+a),11)<1;B=np.mod(xx+.14*yy,12)<1
        f=np.zeros((G,G),np.uint8);f[A]=3;f[B]=2;f[A&B]=1;fr.append(f)
    return (fr,110,K+W+RED+LEAF)
def golds():
    P=K+W+[214,178,84]+[166,126,56]+[116,84,38]+[70,50,24];fr=[];T=14
    for t in range(T):
        g=-10+84*t/(T-1);f=blank()
        for i in range(6):
            x=8+(i%3)*17;y=14+(i//3)*19;m=(xx>=x)&(xx<x+14)&(yy>=y)&(yy<y+14)
            c=2+i if i<4 else 5;d=dith(np.full((G,G),.75-.1*i))>0;f[m&d]=c
            sh=m&(np.abs(xx+yy*.4-g)<2)&d;f[sh]=1
        fr.append(f)
    return (fr,110,P)
def lips():
    fr=[];T=14
    for t in range(T):
        k=.5-.5*np.cos(2*np.pi*t/T);f=blank();f=ell(f,14,4,49,60,0,1);line(f,22,26,28,26);line(f,36,26,42,26);line(f,32,30,30,38);line(f,30,38,33,38)
        f=poly(f,[(24,47),(29,44),(32,45),(35,44),(40,47),(32,51)],2)
        x=28+6*k;put(f,x,48,1);put(f,x+1,48,1);fr.append(f)
    return (fr,130,K+W+RED)
FIFTH=dict(red_light=red_light,neon_words=neon_words,neon_orange=neon_orange,fuchsia=fuchsia,blue_green=blue_green,yellow_black=yellow_black,red_green=red_green,golds=golds,lips=lips)
if __name__=='__main__':
    for k,fn in FIFTH.items():
        o=fn();fr=o[0] if isinstance(o[0],list) else [o[0]]
        write(k,o[0],o[1],o[2])
        f=fr[0];print(k,'colour share %.0f%%'%(100*np.mean(f>1 if max(map(int,[f.max()]))>1 and k!='red_light' else f>0)))
