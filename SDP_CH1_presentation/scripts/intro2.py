# Light daytime intro: the right-hand tower's windows turn amber letter by letter to spell names + IDs.
# Background = the deck's own city plate (image1) under a white veil, so slide text on the left stays readable.
import numpy as np, subprocess, sys
from PIL import Image, ImageFilter
exec(open(__file__.replace('intro2.py', 'font5x7.py')).read())          # F, LINES
plate_path, out, poster = sys.argv[1], sys.argv[2], sys.argv[3]
W, H, FPS = 1920, 1080, 30
rng = np.random.default_rng(16)
plate = Image.open(plate_path).convert('RGB').resize((W, H))
base = np.asarray(plate, np.float32)
base = base * 0.45 + 255 * 0.55                       # same 55 % white veil as the old title slide
CELL = 11; COLS = 15 * 6 - 1 + 4
TX = 1920 - COLS * CELL - 26; TW = COLS * CELL; TY = 120                  # tower: x 1010..1847, top at y 120, runs off the bottom
ROWS = (H - TY) // CELL + 1
TEXT_R0 = 12                                           # first text row inside the facade
on_time = np.full((ROWS, COLS), np.inf); letters = []
for li, txt in enumerate(LINES):
    r0 = TEXT_R0 + li * 9; width = len(txt) * 6 - 1; c0 = (COLS - width) // 2
    for k, ch in enumerate(txt):
        if ch == ' ': continue
        letters.append([(r0 + y, c0 + k * 6 + x) for y in range(7) for x in range(5) if F[ch][y][x] == '1'])
T_START, STEP, FLICK = 1.0, 0.13, 0.18
for i, cells in enumerate(letters):
    for r, c in cells: on_time[r, c] = T_START + i * STEP
T_DONE = T_START + len(letters) * STEP + FLICK; DUR = T_DONE + 2.0
amb = (rng.random((ROWS, COLS)) < 0.035) & np.isinf(on_time)          # a few daytime-lit windows
# tower body (flat style of the plate: slate-grey with a lighter crown)
SLATE, SHADE, CROWN = np.array([172, 183, 200]), np.array([140, 153, 174]), np.array([150, 163, 184])
body = base.copy()
body[TY - 6:, TX - 16:TX + TW + 16] = SLATE
body[TY - 6:, TX + TW + 4:TX + TW + 16] = SHADE                       # shaded edge
body[TY - 46:TY - 6, TX + TW // 2 - 120:TX + TW // 2 + 120] = CROWN    # roof crown
body[TY - 90:TY - 46, TX + TW // 2 - 2:TX + TW // 2 + 2] = SHADE       # mast
for r in range(ROWS):                                                  # all windows "off" (pale glass)
    y0 = TY + r * CELL + 1
    for c in range(COLS):
        x0 = TX + c * CELL + 1
        body[y0:y0 + CELL - 3, x0:x0 + CELL - 3] = [198, 207, 220] if not amb[r, c] else [246, 224, 170]
OFF = body
AMBER_HI, AMBER = np.array([255, 170, 30]), np.array([226, 120, 0])
def frame_at(t):
    f = OFF.copy(); glow = np.zeros_like(f)
    rr, cc = np.where(on_time <= t)
    for r, c in zip(rr, cc):
        dt = t - on_time[r, c]
        lvl = [0.4, 1, 0.25, 1, 0.7, 1][int(dt / FLICK * 6) % 6] if dt < FLICK else 1.0
        y0 = TY + r * CELL + 1; x0 = TX + c * CELL + 1
        col = np.array([198, 207, 220]) * (1 - lvl) + AMBER * lvl
        f[y0 - 1:y0 + CELL - 2, x0 - 1:x0 + CELL - 2] = col
        glow[y0 - 1:y0 + CELL - 2, x0 - 1:x0 + CELL - 1] = AMBER_HI * lvl
    g = np.asarray(Image.fromarray(glow.clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(8)), np.float32)
    f = f + g * 0.25
    return Image.fromarray(f.clip(0, 255).astype(np.uint8))
p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
last = None
for i in range(int(DUR * FPS) + 1):
    last = frame_at(i / FPS); p.stdin.write(last.tobytes())
p.stdin.close(); p.wait(); last.save(poster)
print('duration', round(DUR, 2))
