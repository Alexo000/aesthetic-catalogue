import numpy as np, math
from PIL import Image
from numpy.fft import fftfreq, ifft2, ifftn
G=64
OUT='site/plates'
PAL=[0,0,0, 244,243,238, 255,42,26, 4,6,24]
def blank(n=G): return np.zeros((n,n),np.uint8)
def put(a,x,y,c=1):
    x=int(round(x));y=int(round(y)); n=a.shape[0]
    if 0<=x<n and 0<=y<n: a[y,x]=c
def line(a,x0,y0,x1,y1,c=1):
    x0,y0,x1,y1=[int(round(v)) for v in (x0,y0,x1,y1)]
    dx=abs(x1-x0);dy=-abs(y1-y0);sx=1 if x0<x1 else -1;sy=1 if y0<y1 else -1;e=dx+dy
    while True:
        put(a,x0,y0,c)
        if x0==x1 and y0==y1: break
        e2=2*e
        if e2>=dy: e+=dy;x0+=sx
        if e2<=dx: e+=dx;y0+=sy
def rect(a,x0,y0,x1,y1,c=1):
    x0,y0,x1,y1=[int(round(v)) for v in (x0,y0,x1,y1)]
    for x,y,X,Y in ((x0,y0,x1,y0),(x0,y1,x1,y1),(x0,y0,x0,y1),(x1,y0,x1,y1)): line(a,x,y,X,Y,c)
def fill(a,x0,y0,x1,y1,c=1):
    n=a.shape[0]; a[max(int(y0),0):min(int(y1)+1,n),max(int(x0),0):min(int(x1)+1,n)]=c
def bayer(k):
    if k==0: return np.array([[0]])
    m=bayer(k-1); return np.block([[4*m,4*m+2],[4*m+3,4*m+1]])
B8=(bayer(3)+.5)/64.
# a clustered dot screen, the look of printed comics
CL=np.array([[12,5,6,13],[4,0,1,7],[11,3,2,8],[15,10,9,14]],float); CL=(CL+.5)/16
def dith(v,M=B8):
    n=v.shape[0]; h=M.shape[0]; t=np.tile(M,(n//h+1,n//h+1))[:n,:n]
    return (v>t).astype(np.uint8)
def noise2(n,beta,seed):
    r=np.random.default_rng(seed); f=fftfreq(n)*n; fx,fy=np.meshgrid(f,f); k=np.hypot(fx,fy); k[0,0]=1
    z=np.real(ifft2(k**(-beta)*np.exp(2j*np.pi*r.random((n,n))))); return (z-z.mean())/z.std()
def noise3(n,nz,beta,seed):
    r=np.random.default_rng(seed); fx,fy,fz=np.meshgrid(fftfreq(n)*n,fftfreq(n)*n,fftfreq(nz)*nz,indexing='ij')
    k=np.sqrt(fx**2+fy**2+fz**2);k[0,0,0]=1
    z=np.real(ifftn(k**(-beta)*np.exp(2j*np.pi*r.random((n,n,nz))))); return (z-z.mean())/z.std()
def write(name,frames,dur):
    if not isinstance(frames,list): frames=[frames]
    def im(f):
        i=Image.fromarray(np.asarray(f,np.uint8),'P'); i.putpalette(PAL+[0]*(768-len(PAL))); return i
    ims=[im(f) for f in frames]
    if len(ims)==1: ims[0].save(f'{OUT}/{name}.png',optimize=True); return
    ims[0].save(f'{OUT}/{name}.gif',save_all=True,append_images=ims[1:],duration=dur,loop=0,disposal=1,optimize=False)
