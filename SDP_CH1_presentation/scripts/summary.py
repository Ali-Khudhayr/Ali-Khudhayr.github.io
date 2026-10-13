import sys, subprocess, numpy as np
from PIL import Image
src, out, poster = sys.argv[1], sys.argv[2], sys.argv[3]
keep = [1,4,5,6,7,8,9,11,12,14,15,17,18,19,20,21,22,23]   # content slides (no intro / dividers / final)
ims = [np.asarray(Image.open(f'{src}/s-{n:02d}.png').convert('RGB').resize((1280,720)), np.float32) for n in keep]
FPS, HOLD, FADE = 25, 2.4, 0.6
p = subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(FPS),'-i','-',
     '-c:v','libx264','-pix_fmt','yuv420p','-crf','24','-preset','slow','-movflags','+faststart',out], stdin=subprocess.PIPE)
for i, im in enumerate(ims):
    nxt = ims[(i + 1) % len(ims)]          # last fades into first -> seamless loop
    for k in range(int(HOLD * FPS)):
        p.stdin.write(im.astype(np.uint8).tobytes())
    for k in range(int(FADE * FPS)):
        a = (k + 1) / (FADE * FPS); p.stdin.write((im * (1 - a) + nxt * a).astype(np.uint8).tobytes())
p.stdin.close(); p.wait()
Image.fromarray(ims[0].astype(np.uint8)).save(poster)
print(len(ims) * (HOLD + FADE), 's')
