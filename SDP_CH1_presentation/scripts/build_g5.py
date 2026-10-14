# Merge 6+7 (comparison) and 8+9 (two-function slide) in the team's F_v5.
import os, re, shutil, sys, uuid
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
SRC, D = sys.argv[1], sys.argv[2]
if os.path.exists(D): shutil.rmtree(D)
shutil.copytree(SRC, D); P = D + '/ppt/'
def rd(f): return open(P + f, encoding='utf-8').read()
def wr(f, s): open(P + f, 'w', encoding='utf-8').write(s)
LAYOUT = ('rIdL', REL_LAYOUT, '../slideLayouts/slideLayout7.xml')
IMG = {'meter': 'image20.png', 'check': 'image27.png', 'sort': 'image36.png', 'bell': 'image26.png', 'pulse': 'image12.png',
       'plug': 'image29.png', 'ac': 'image21.png', 'fridge': 'image22.png', 'heater': 'image23.png', 'washer': 'image24.png'}
CY, CH, CW = 1.95, 4.45, 5.55
def card(b, x, tint, fill, icon, title, sub, rows, badge):
    """b: base id; rows: list of text; badge(i, bx, by) -> list of shapes for the row marker."""
    k = [shape(b, f'card{b}', x, CY, CW, CH, fill),
         shape(b + 1, f'oval{b}', x + 0.35, CY + 0.35, 0.8, 0.8, tint, prst='ellipse'),
         pic(b + 2, f'icon{b}', f'rIdI_{icon}', x + 0.54, CY + 0.54, 0.42, 0.42, icon),
         text(b + 3, f'title{b}', x + 1.4, CY + 0.36, CW - 1.6, 0.45, [para([run(title, 22, INK, 'Bahnschrift SemiBold')])]),
         text(b + 4, f'sub{b}', x + 1.4, CY + 0.82, CW - 1.6, 0.35, [para([run(sub, 14, SLATE, 'Segoe UI')])])]
    for i, t in enumerate(rows):
        y = CY + 1.65 + i * 0.88; ib = b + 10 + i * 4
        k += badge(i, ib, x + 0.4, y)
        k.append(text(ib + 3, f'row{ib}', x + 1.05, y - 0.02, CW - 1.3, 0.5, [para([run(t, 17, INK, 'Segoe UI')])], anchor='ctr'))
    return group(b - 1, f'g{b}', x, CY, CW, CH, k)
def q_badge(i, ib, bx, by):
    return [shape(ib, f'qb{ib}', bx, by, 0.44, 0.44, 'FEE2E2', prst='ellipse'),
            text(ib + 1, f'qt{ib}', bx, by + 0.03, 0.44, 0.38, [para([run('?', 16, RED, 'Bahnschrift SemiBold')], 'ctr')], anchor='ctr')]
def chk_badge(i, ib, bx, by):
    return [shape(ib, f'cb{ib}', bx, by, 0.44, 0.44, 'CCFBF1', prst='ellipse'),
            pic(ib + 1, f'ci{ib}', 'rIdI_check', bx + 0.08, by + 0.08, 0.28, 0.28, 'check')]
def num_badge(col):
    def f(i, ib, bx, by):
        return [shape(ib, f'nb{ib}', bx, by, 0.44, 0.44, col, prst='ellipse'),
                text(ib + 1, f'nt{ib}', bx, by + 0.04, 0.44, 0.36, [para([run(str(i + 1), 15, 'FFFFFF', 'Bahnschrift SemiBold')], 'ctr')], anchor='ctr')]
    return f
def notes_rel(n):
    return ('rIdN', REL_NOTES, re.search(r'Target="(\.\./notesSlides/notesSlide\d+\.xml)"', rd(f'slides/_rels/slide{n}.xml.rels')).group(1))
def img_rels(keys): return [(f'rIdI_{k}', REL_IMG, '../media/' + IMG[k]) for k in keys]
# ---- slide 6: comparison (old 6 + 7)
ch = header('01 · INTRODUCTION', 'One total vs. per-appliance visibility', '#')
ch.append(card(11, 0.75, 'E2E8F0', CARD, 'meter', 'Conventional meter', 'One number for the whole house',
               ['Which appliance uses the most?', 'Which load can wait?', 'Which one is misbehaving?'], q_badge))
ch.append(flat(60, 'arrow', 6.42, 3.95, 0.48, 0.5, '0F766E', prst='rightArrow'))
ch.append(card(71, 7.03, 'CCFBF1', 'E6F7F5', 'plug', 'Per-appliance monitoring', 'Every load measured on its own',
               ['V · I · P · kWh · ON/OFF per load', 'Cost per appliance → stay in budget', 'Essentials stay ON · early warnings'], chk_badge))
ch.append(text(99, 'tag', 0.75, 6.52, 11.83, 0.35, [para([run('Not a luxury — ', 15, SLATE, 'Segoe UI Semibold'), run('a need.', 15, AMBER, 'Segoe UI Semibold')], 'ctr')]))
wr('slides/slide6.xml', slide(ch, timing(fade_chain([10, 60, 70, 99], 150, 300))))
wr('slides/_rels/slide6.xml.rels', rels([LAYOUT, notes_rel(6)] + img_rels(['meter', 'plug', 'check'])))
# ---- slide 8: priority control (core) + abnormal warning (supporting) (old 8 + 9)
ch = header('01 · INTRODUCTION', 'Priority control & abnormal warning', '#')
ch.append(card(11, 0.75, 'FEF3C7', CARD, 'sort', 'Priority-based control', 'Core function',
               ['User sets load priorities', 'Demand > limit → shed lowest first', 'Essential loads stay ON'], num_badge(INK)))
ch.append(card(71, 7.03, 'FEE2E2', CARD, 'bell', 'Abnormal warning', 'Supporting function',
               ['Each load vs. its own baseline', 'Deviation → warn the user', 'Sub-metering → reliable detection'], num_badge(RED)))
ch.append(text(99, 'src', 0.75, 6.55, 11.83, 0.3, [para([run('Priority scheduling concept: [4]  ·  Appliance anomaly detection: Rashid et al. [5]', 11, SLATE, 'Segoe UI', i=1)])]))
wr('slides/slide8.xml', slide(ch, timing(fade_chain([10, 70], 150, 350))))
wr('slides/_rels/slide8.xml.rels', rels([LAYOUT, notes_rel(8)] + img_rels(['sort', 'bell'])))
# ---- drop old 7 and 9 from the show
pres = rd('presentation.xml'); prels = rd('_rels/presentation.xml.rels')
rid = {n: r for r, n in re.findall(r'Id="(rId\d+)"[^>]*Target="slides/slide(\d+)\.xml"', prels)}
for n in ('7', '9'):
    pres, c = re.subn(r'<p:sldId id="\d+" r:id="%s"/>' % rid[n], '', pres); assert c == 1
wr('presentation.xml', pres)
# ---- live slide numbers, correct cached values
rmap = {r: n for n, r in rid.items()}
for pos, r in enumerate(re.findall(r'<p:sldId id="\d+" r:id="(rId\d+)"/>', rd('presentation.xml')), 1):
    f = f'slides/slide{rmap[r]}.xml'; s = rd(f)
    def fix(m):
        sp = m.group(0)
        sp = re.sub(r'<a:r><a:rPr([^>]*)>(.*?)</a:rPr><a:t>[^<]*</a:t></a:r>',
                    lambda q: f'<a:fld id="{{{str(uuid.uuid4()).upper()}}}" type="slidenum"><a:rPr lang="en-US"{re.sub(r" lang=\"[^\"]*\"", "", q.group(1))}>{q.group(2)}</a:rPr><a:t>{pos}</a:t></a:fld>', sp, count=1)
        return re.sub(r'(<a:fld [^>]*type="slidenum">.*?<a:t>)[^<]*(</a:t>)', lambda q: q.group(1) + str(pos) + q.group(2), sp, flags=re.S)
    wr(f, re.sub(r'<p:sp><p:nvSpPr><p:cNvPr id="\d+" name="pageno"/>.*?</p:sp>', fix, s, flags=re.S))
print('done')
