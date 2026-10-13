# Night-city intro: tower windows light up letter by letter to spell names + IDs.
import numpy as np, subprocess, sys
from PIL import Image, ImageFilter
W,H,FPS=1920,1080,30
rng=np.random.default_rng(16)
F={ # 5x7 pixel font
'A':["01110","10001","10001","11111","10001","10001","10001"],
'B':["11110","10001","10001","11110","10001","10001","11110"],
'D':["11110","10001","10001","10001","10001","10001","11110"],
'E':["11111","10000","10000","11110","10000","10000","11111"],
'F':["11111","10000","10000","11110","10000","10000","10000"],
'H':["10001","10001","10001","11111","10001","10001","10001"],
'I':["11111","00100","00100","00100","00100","00100","11111"],
'K':["10001","10010","10100","11000","10100","10010","10001"],
'L':["10000","10000","10000","10000","10000","10000","11111"],
'M':["10001","11011","10101","10101","10001","10001","10001"],
'O':["01110","10001","10001","10001","10001","10001","01110"],
'R':["11110","10001","10001","11110","10100","10010","10001"],
'S':["01111","10000","10000","01110","00001","00001","11110"],
'U':["10001","10001","10001","10001","10001","10001","01110"],
'Y':["10001","10001","01010","00100","00100","00100","00100"],
'1':["00100","01100","00100","00100","00100","00100","01110"],
'2':["01110","10001","00001","00010","00100","01000","11111"],
'3':["11110","00001","00001","01110","00001","00001","11110"],
'4':["00010","00110","01010","10010","11111","00010","00010"],
'5':["11111","10000","11110","00001","00001","10001","01110"],
'6':["00110","01000","10000","11110","10001","10001","01110"],
'8':["01110","10001","10001","01110","10001","10001","01110"],
'9':["01110","10001","10001","01111","00001","00010","01100"],
' ':["00000"]*7,
}
LINES=["ALI KHUDHAYR","2343192","MOHAMMAD KASSEM","2364954","OMAR BAFLAH","2343198"]
COLS=15*6-1+6; ROWS=6*7+5*2+6          # facade window grid (with margins)
CELL=13; BW,BH=COLS*CELL,ROWS*CELL
BX=(W-BW)//2; BY=H-150-BH              # building top-left
# map letters -> window cells, in reading order
letters=[]                              # list of (label, [(r,c),...])
for li,txt in enumerate(LINES):
    r0=3+li*9; width=len(txt)*6-1; c0=(COLS-width)//2
    for k,ch in enumerate(txt):
        if ch==' ': continue
        cells=[(r0+y,c0+k*6+x) for y in range(7) for x in range(5) if F[ch][y][x]=='1']
        letters.append(cells)
T_START=1.2; STEP=0.13; FLICK=0.18
on_time=np.full((ROWS,COLS),np.inf)
for i,cells in enumerate(letters):
    for (r,c) in cells: on_time[r,c]=T_START+i*STEP
T_DONE=T_START+len(letters)*STEP+FLICK
DUR=T_DONE+2.5
# ambient windows of the tower (random, dim warm/cool), excluding letter cells
amb=(rng.random((ROWS,COLS))<0.10)&np.isinf(on_time)
amb_col=np.where(rng.random((ROWS,COLS))<0.7,1,0)
# ---------- static background ----------
y=np.linspace(0,1,H)[:,None]
sky=np.zeros((H,W,3),np.float32)
top=np.array([6,10,24]);mid=np.array([18,32,64]);hor=np.array([70,62,80])
t=np.clip(y/0.85,0,1)
col=np.where(t<0.6,top+(mid-top)*(t/0.6),mid+(hor-mid)*((t-0.6)/0.4))
sky[:]=col[:,None,:]
stars=rng.random((H,W))<0.0009; stars[int(H*0.55):]=False
sky[stars]=[200,210,235]
img=Image.fromarray(sky.clip(0,255).astype(np.uint8))
bg=np.array(img,np.float32)
def skyline(layer_y,hmin,hmax,col,dens,winp,seed):
    r=np.random.default_rng(seed); x=0
    while x<W:
        w=int(r.integers(60,170)); h=int(r.integers(hmin,hmax))
        bg[layer_y-h:layer_y, x:x+w]=col
        for wy in range(layer_y-h+10,layer_y-8,14):
            for wx in range(x+8,x+w-8,12):
                if r.random()<winp:
                    c=np.array([255,196,110]) if r.random()<.75 else np.array([170,200,255])
                    bg[wy:wy+6,wx:wx+5]=c*r.uniform(.35,.8)
        x+=w+int(r.integers(0,12))
skyline(H-150,180,420,np.array([22,27,42]),1,0.10,3)
skyline(H-150,90,260,np.array([14,18,30]),1,0.16,5)
# ground / street
bg[H-150:]=np.array([10,12,20]); 
for x in range(0,W,90): bg[H-92:H-88,x:x+45]=[60,60,70]
base=bg.copy()
# tower body
tower=np.zeros((BH+40,BW+40,3),np.float32)
def draw_tower(frame):
    frame[BY-30:BY+BH,BX-20:BX+BW+20]=[28,34,50]
    frame[BY-30:BY-18,BX-26:BX+BW+26]=[40,48,66]           # roof slab
    frame[BY-70:BY-30,BX+BW//2-40:BX+BW//2+40]=[30,36,52]   # roof room
    frame[BY-150:BY-70,BX+BW//2-3:BX+BW//2+3]=[60,66,80]    # antenna
    frame[BY:BY+BH,BX-20:BX-8]=[22,27,40]; frame[BY:BY+BH,BX+BW+8:BX+BW+20]=[22,27,40]
draw_tower(base)
base_img=base
def frame_at(t):
    f=base_img.copy()
    glow=np.zeros_like(f)
    # windows
    for r in range(ROWS):
        y0=BY+r*CELL+2
        for c in range(COLS):
            x0=BX+c*CELL+2
            ot=on_time[r,c]
            if t>=ot:
                dt=t-ot
                if dt<FLICK: lvl=[0.3,1,0.15,1,0.6,1][int(dt/FLICK*6)%6]
                else: lvl=1.0
                col=np.array([255,214,140])*lvl
                f[y0:y0+CELL-4,x0:x0+CELL-4]=col
                glow[y0-2:y0+CELL-2,x0-2:x0+CELL-2]=np.array([255,170,60])*lvl
            elif amb[r,c]:
                col=np.array([150,110,60]) if amb_col[r,c] else np.array([70,90,130])
                f[y0:y0+CELL-4,x0:x0+CELL-4]=col*0.55
            else:
                f[y0:y0+CELL-4,x0:x0+CELL-4]=[16,20,32]
    # blinking roof beacon
    if int(t*1.4)%2==0:
        bx,by=BX+BW//2,BY-152
        f[by-5:by+5,bx-5:bx+5]=[255,60,60]; glow[by-14:by+14,bx-14:bx+14]=[255,40,40]
    g=Image.fromarray(glow.clip(0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14))
    f=f+np.array(g,np.float32)*0.9
    # reflection on wet street
    refl=f[H-150-120:H-150][::-1]*0.22
    f[H-150:H-30]+=refl
    # slow push-in
    z=1.0+0.035*min(t/DUR,1)
    im=Image.fromarray(f.clip(0,255).astype(np.uint8))
    cw,ch=int(W/z),int(H/z); x0=(W-cw)//2; y0=(H-ch)//2+int(20*(z-1)*10)
    im=im.crop((x0,y0,x0+cw,y0+ch)).resize((W,H),Image.LANCZOS)
    return im
out=sys.argv[1]; poster=sys.argv[2]
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
   '-c:v','libx264','-pix_fmt','yuv420p','-profile:v','high','-crf','20','-movflags','+faststart',out],stdin=subprocess.PIPE)
n=int(DUR*FPS); last=None
for i in range(n):
    last=frame_at(i/FPS); p.stdin.write(last.tobytes())
p.stdin.close(); p.wait()
last.save(poster)
print('duration',DUR,'letters',len(letters))
