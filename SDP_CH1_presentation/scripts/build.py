import os, re, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
SRC, D = sys.argv[1], sys.argv[2]          # original unpacked dir, output dir
SUMMARY = sys.argv[3] if len(sys.argv) > 3 else None   # (mp4, poster png) prefix
WORK = os.path.dirname(os.path.abspath(__file__))
if os.path.exists(D): shutil.rmtree(D)
shutil.copytree(SRC, D)
P = D + '/ppt/'
def rd(f): return open(P + f, encoding='utf-8').read()
def wr(f, s): open(P + f, 'w', encoding='utf-8').write(s)
def notes_rel(n):
    m = re.search(r'Target="(\.\./notesSlides/notesSlide\d+\.xml)"', rd(f'slides/_rels/slide{n}.xml.rels'))
    return ('rIdN', REL_NOTES, m.group(1))
LAYOUT = ('rIdL', REL_LAYOUT, '../slideLayouts/slideLayout7.xml')
def cp_media(src, name): shutil.copy(src, P + 'media/' + name); return '../media/' + name
ICON = {  # existing icon files
 'home_amberd':'image16.png','ac_amberd':'image17.png','trend_redd':'image44.png','chart_teald':'image13.png',
 'pulse_amberd':'image28.png','shield_redd':'image21.png','card_amberd':'image29.png','power_teald':'image30.png'}
ORDER = []   # final order of slide files
# ------------------------------------------------------------ 1. intro video slide (reuses slide4.xml)
iv = cp_media(WORK + '/intro.mp4', 'media9.mp4'); ip = cp_media(WORK + '/intro_poster.png', 'image66.png')
TL = 0.6; TW_ = 5.15
kids1 = [video(2, 'vid_intro', 'rIdM', 'rIdV', 'rIdP', 0, 0, 13.3333, 7.5,
               'Opening: the tower windows spell the team names and university IDs'),
         shape(3, 'logo_bg', TL, 0.6, 1.0, 1.0, 'FFFFFF', adj=17142),
         pic(4, 'logo', 'rIdLogo', TL + 0.05, 0.65, 0.9, 0.9, 'King Abdulaziz University logo'),
         text(5, 'kick', TL + 1.25, 0.7, 4.2, 0.8, [para([run('EE499  SENIOR DESIGN PROJECT', 13, AMBER, spc=200)]),
                                                   para([run('Report 1 — Problem & Design Requirements', 13, SLATE, 'Segoe UI')])]),
         text(6, 't1', TL, 1.9, TW_, 1.3, [para([run('Smart Home', 34, INK, 'Bahnschrift SemiBold')], lnpct=92000),
                                           para([run('Energy Management', 34, INK, 'Bahnschrift SemiBold')], lnpct=92000)]),
         text(7, 't2', TL, 3.15, TW_, 0.5, [para([run('with Priority-Based Load Control', 22, AMBER, 'Bahnschrift SemiBold')])]),
         text(8, 'team', TL, 4.15, TW_, 0.3, [para([run('TEAM 16  ·  PME', 12, AMBER, spc=200)])]),
         text(9, 'adv_k', TL, 4.7, TW_, 0.3, [para([run('ADVISOR & CUSTOMER', 13, AMBER, spc=300)])]),
         text(10, 'adv', TL, 5.05, TW_, 0.45, [para([run('Dr. Fahd Hariri', 24, INK)])]),
         text(11, 'uni', TL, 5.55, TW_, 0.6, [para([run('Electrical and Computer Engineering', 14, SLATE, 'Segoe UI Semibold')]),
                                            para([run('King Abdulaziz University  ·  Fall 2026', 14, SLATE, 'Segoe UI Semibold')])])]
def intro_steps(t):
    return [play(t, 2, 0, 10500)] + [fadeup(t, sid, 150 + i * 220) for i, sid in enumerate([3, 4, 5, 6, 7, 8, 9, 10, 11])]
wr('slides/slide4.xml', slide(kids1, timing(intro_steps, [(2, False, True)])))
wr('slides/_rels/slide4.xml.rels', rels([LAYOUT, notes_rel(4), ('rIdM', REL_MEDIA, iv), ('rIdV', REL_VID, iv), ('rIdP', REL_IMG, ip),
                                         ('rIdLogo', REL_IMG, '../media/image2.png')]))
# ------------------------------------------------------------ stat-card slides (merge of old 4-9)
def stat_slide(n, kicker, title, cards, src_lines):
    ch = header(kicker, title, '#')
    rl = [LAYOUT, notes_rel(n)]
    cw, gap, x0, y0, hgt = (11.83 - 0.6) / 3, 0.3, 0.75, 1.95, 4.15
    gids = []
    for i, (icon, tint, big, col, label, sub) in enumerate(cards):
        x = x0 + i * (cw + gap); b = 10 + i * 10; rid = f'rIdI{i}'
        rl.append((rid, REL_IMG, '../media/' + ICON[icon]))
        kids = [shape(b + 1, f'card{i}', x, y0, cw, hgt, CARD),
                shape(b + 2, f'oval{i}', x + 0.35, y0 + 0.35, 0.85, 0.85, tint, prst='ellipse'),
                pic(b + 3, f'icon{i}', rid, x + 0.535, y0 + 0.535, 0.48, 0.48, icon + '.png'),
                text(b + 4, f'big{i}', x + 0.35, y0 + 1.4, cw - 0.6, 1.0, [para([run(big, 54, col, 'Bahnschrift SemiBold')])]),
                text(b + 5, f'label{i}', x + 0.35, y0 + 2.5, cw - 0.6, 0.75, [para([run(label, 20, INK)], lnpct=95000)]),
                text(b + 6, f'sub{i}', x + 0.35, y0 + 3.35, cw - 0.6, 0.6, [para([run(sub, 15, SLATE, 'Segoe UI')])])]
        ch.append(group(b, f'stat{i}', x, y0, cw, hgt, kids)); gids.append(b)
    if src_lines:
        ch.append(text(50, 'src', 0.75, 6.28, 11.83, 0.6, [para([run(s, 10.5, SLATE, 'Segoe UI', i=1)]) for s in src_lines]))
    wr(f'slides/slide{n}.xml', slide(ch, timing(fade_chain(gids, 150, 250))))
    wr(f'slides/_rels/slide{n}.xml.rels', rels(rl))
stat_slide(5, '01 · INTRODUCTION', 'Where household electricity goes', [
    ('home_amberd', 'FEF3C7', '47 %', AMBER, 'of Saudi electricity → homes', 'Residential share of national consumption'),
    ('ac_amberd', 'FEF3C7', '≈ 70 %', AMBER, 'of home electricity → air-conditioning', 'Highest share worldwide'),
    ('trend_redd', 'FEE2E2', '+67 %', RED, 'per extra kWh above 6,000 kWh / month', '18 → 30 halalas / kWh')], [])
stat_slide(7, '01 · INTRODUCTION', 'What the single total hides', [
    ('chart_teald', 'CCFBF1', '14 %', TEAL, 'median electricity saved', 'with real-time, per-appliance feedback'),
    ('pulse_amberd', 'FEF3C7', '5–15 %', AMBER, 'extra AC energy from a dirty filter', 'Hidden in the total — visible per appliance'),
    ('shield_redd', 'FEE2E2', '≈ 53', RED, 'house fires / day in KSA', '#1 cause: electrical incidents')],
    ['14 %: ACEEE meta-review, 57 studies (2010) — an indication, not a promise.  ·  5–15 %: U.S. DOE, Energy Saver, “Maintaining your air conditioner”.',
     '53 / day: 193,437 house fires in 10 years (Civil Defense via Arab News, 2015) ÷ 3,650 days.'])
# ------------------------------------------------------------ merge of old 10 + 11 (reuses slide10.xml)
s10 = rd('slides/slide10.xml')
def grab(s, sid):
    m = re.search(r'<p:(sp|grpSp|pic)><p:nv\w+><p:cNvPr id="%d"' % sid, s); tag = m.group(1); depth = 0
    for mm in re.finditer(r'<(/?)p:%s>' % tag, s[m.start():]):
        depth += -1 if mm.group(1) else 1
        if depth == 0: return s[m.start():m.start() + mm.end()]
def move_group(g, x, y, w, h):
    return re.sub(r'(<p:grpSpPr><a:xfrm>)<a:off x="\d+" y="\d+"/><a:ext cx="\d+" cy="\d+"/>',
                  lambda m: m.group(1) + f'<a:off x="{E(x)}" y="{E(y)}"/><a:ext cx="{E(w)}" cy="{E(h)}"/>', g, count=1)
sc = 0.75; aw, ah, mw, mh = 2.7 * sc, 1.98 * sc, 3.0 * sc, 3.25 * sc
ax1 = 0.75; mx = ax1 + aw + 0.25; ax2 = mx + mw + 0.25; ay1, ay2, my = 2.45, 2.45 + ah + 0.36, 2.8
ch = header('01 · INTRODUCTION', 'One meter. One number.', '#', ids=(90, 91, 92, 93))
ch += [move_group(grab(s10, 8), mx, my, mw, mh), move_group(grab(s10, 14), ax1, ay1, aw, ah), move_group(grab(s10, 20), ax1, ay2, aw, ah),
       move_group(grab(s10, 26), ax2, ay1, aw, ah), move_group(grab(s10, 32), ax2, ay2, aw, ah)]
rx, ry, rw, rh = 7.85, 1.95, 4.73, 4.45
rows = [('card_amberd', 'FEF3C7', 'Cost', 'Which appliance? → see the bill, stay in budget'),
        ('power_teald', 'CCFBF1', 'Continuity', 'Which can wait? → essentials stay ON'),
        ('shield_redd', 'FEE2E2', 'Safety', 'Which misbehaves? → warn early, fail safe')]
kids = [shape(61, 'need_card', rx, ry, rw, rh, CARD),
        text(62, 'need_title', rx + 0.35, ry + 0.3, rw - 0.6, 0.55, [para([run('Not a luxury. ', 26, INK, 'Bahnschrift SemiBold'), run('A need.', 26, AMBER, 'Bahnschrift SemiBold')])])]
rl10 = rd('slides/_rels/slide10.xml.rels')
extra = ''
for i, (icon, tint, ttl, sub) in enumerate(rows):
    yy = ry + 1.1 + i * 1.08; b = 70 + i * 5
    extra += f'<Relationship Id="rIdX{i}" Type="{REL_IMG}" Target="../media/{ICON[icon]}"/>'
    kids += [shape(b, f'need_oval{i}', rx + 0.35, yy, 0.75, 0.75, tint, prst='ellipse'),
             pic(b + 1, f'need_icon{i}', f'rIdX{i}', rx + 0.515, yy + 0.165, 0.42, 0.42, icon + '.png'),
             text(b + 2, f'need_t{i}', rx + 1.3, yy - 0.02, rw - 1.55, 0.4, [para([run(ttl, 20, INK, 'Bahnschrift SemiBold')])]),
             text(b + 3, f'need_s{i}', rx + 1.3, yy + 0.38, rw - 1.55, 0.5, [para([run(sub, 14, SLATE, 'Segoe UI')])])]
ch.append(group(60, 'need', rx, ry, rw, rh, kids))
wr('slides/slide10.xml', slide(ch, timing(fade_chain([8, 14, 20, 26, 32, 60], 150, 200))))
wr('slides/_rels/slide10.xml.rels', rl10.replace('</Relationships>', extra + '</Relationships>'))
# ------------------------------------------------------------ slide 12: reword, dashes, no repetition
s = rd('slides/slide12.xml')
for sid in (18, 22, 26, 30, 32, 3): s = s.replace(grab(s, sid), '')
s = s.replace('<a:t>Total only</a:t>', '<a:t>Whole-house total only</a:t>')
rid_of = {d: r for d, r in re.findall(r'descr="([^"]+)"[^>]*/>.*?r:embed="(rId\d+)"', s)}
kids = []
apps = [('ac_teald.png', 'Air conditioner'), ('fridge_teald.png', 'Refrigerator'), ('heater_teald.png', 'Water heater'), ('washer_teald.png', 'Washing machine')]
r12 = rd('slides/_rels/slide12.xml.rels')
img_for = {'ac_teald.png': 'image32.png', 'fridge_teald.png': 'image33.png', 'heater_teald.png': 'image34.png', 'washer_teald.png': 'image35.png'}
add = ''
for i, (ic, nm) in enumerate(apps):
    x = 6.8 + (i % 2) * 2.85; y = 2.95 + (i // 2) * 0.68; b = 41 + i * 2
    add += f'<Relationship Id="rIdA{i}" Type="{REL_IMG}" Target="../media/{img_for[ic]}"/>'
    kids += [pic(b, f'app_icon{i}', f'rIdA{i}', x, y, 0.5, 0.5, ic),
             text(b + 1, f'app_name{i}', x + 0.65, y + 0.07, 2.1, 0.4, [para([run(nm, 17, INK)])])]
kids.append(text(55, 'measured_k', 6.8, 4.45, 5.4, 0.3, [para([run('MEASURED FOR EACH APPLIANCE', 12, TEAL, spc=200)])]))
kids.append(text(56, 'measured', 6.8, 4.85, 5.4, 1.35, [para([run('–  Voltage (V) and current (I)', 17, INK, 'Segoe UI')], after=500),
                                                       para([run('–  Power (P) and energy (kWh)', 17, INK, 'Segoe UI')], after=500),
                                                       para([run('–  ON / OFF status', 17, INK, 'Segoe UI')])]))
s = s.replace('</p:spTree>', group(40, 'monitoring', 6.8, 2.95, 5.65, 3.25, kids) + pageno(3, '#') + '</p:spTree>')
s = re.sub(r'<p:timing>.*</p:timing>', timing(fade_chain([10, 11, 14, 40], 150, 220)), s, flags=re.S)
wr('slides/slide12.xml', s); wr('slides/_rels/slide12.xml.rels', r12.replace('</Relationships>', add + '</Relationships>'))
# ------------------------------------------------------------ slide 25: C-02 → C-04, C-03 → C-02 (C-04 → C-03), in order
s = rd('slides/slide25.xml')
s = s.replace(grab(s, 31), '')
s = s.replace('C-02  ·  SCHEDULE', 'C-04  ·  SCHEDULE').replace('C-03  ·  SCOPE', 'C-02  ·  SCOPE').replace('C-04  ·  LAB POWER', 'C-03  ·  LAB POWER')
assert s.count('C-04  ·  SCHEDULE') == 1 and s.count('C-02  ·  SCOPE') == 1 and s.count('C-03  ·  LAB POWER') == 1
def shift_group(s, sid, x, y):
    g = grab(s, sid)
    g2 = re.sub(r'(<p:grpSpPr><a:xfrm>)<a:off x="\d+" y="\d+"/>', lambda m: m.group(1) + f'<a:off x="{E(x)}" y="{E(y)}"/>', g, count=1)
    return s.replace(g, g2)
s = shift_group(s, 13, 0.75, 4.3)    # schedule (now C-04) -> row 2, col 1
s = shift_group(s, 17, 4.79, 2.0)    # scope (now C-02)    -> row 1, col 2
s = shift_group(s, 21, 8.83, 2.0)    # lab power (now C-03)-> row 1, col 3
s = re.sub(r'<p:timing>.*</p:timing>', timing(fade_chain([9, 17, 21, 13, 25, 29], 150, 180)), s, flags=re.S)
wr('slides/slide25.xml', s)
# ------------------------------------------------------------ slide 26: icons for every standard, fit long title
s = rd('slides/slide26.xml'); s = s.replace(grab(s, 32), '')
r26 = rd('slides/_rels/slide26.xml.rels'); add = ''
badges = [(7, 8, 1.05, 2.33, 'std_controls'), (13, 14, 7.11, 2.33, 'std_meter'), (19, 20, 1.05, 4.53, 'std_wiring'), (25, 26, 7.11, 4.53, 'std_lv')]
for k, (bid, tid, bx, by, ic) in enumerate(badges):
    name = f'image{68 + k}.png'; cp_media(f'{WORK}/{ic}.png', name)
    add += f'<Relationship Id="rIdS{k}" Type="{REL_IMG}" Target="../media/{name}"/>'
    t = grab(s, tid)
    t2 = re.sub(r'<a:off x="\d+" y="\d+"/><a:ext cx="\d+" cy="\d+"/>', f'<a:off x="{E(bx)}" y="{E(by + 0.84)}"/><a:ext cx="{E(1.25)}" cy="{E(0.3)}"/>', t, count=1)
    t2 = re.sub(r'sz="\d+"', 'sz="1300"', t2)
    s = s.replace(t, t2 + pic(90 + k, f'std_icon{k}', f'rIdS{k}', bx + 0.355, by + 0.2, 0.54, 0.54, ic + '.png'))
for tid in (9, 15, 21, 27):
    t = grab(s, tid); s = s.replace(t, t.replace('sz="2400"', 'sz="2100"'))
wr('slides/slide26.xml', s); wr('slides/_rels/slide26.xml.rels', r26.replace('</Relationships>', add + '</Relationships>'))
# ------------------------------------------------------------ slide 21: subtitle on one line, clear of the rail
s = rd('slides/slide21.xml'); t = grab(s, 4)
s = s.replace(t, re.sub(r'<a:ext cx="7315200"', f'<a:ext cx="{E(11.5)}"', t, count=1)); wr('slides/slide21.xml', s)
# ------------------------------------------------------------ final slide: thanks + looping summary + priority control video
r29 = rd('slides/_rels/slide29.xml.rels'); s29 = rd('slides/slide29.xml')
bgvid = grab(s29, 7); veil = grab(s29, 2)
pp = '../media/image65.png'
sv_mp4, sv_png = (SUMMARY + '.mp4', SUMMARY + '.png') if SUMMARY else (WORK + '/intro.mp4', WORK + '/intro_poster.png')
sv = cp_media(sv_mp4, 'media10.mp4'); sp_ = cp_media(sv_png, 'image67.png')
L = 0.75; VW = (11.83 - 0.3) / 2; VH = VW * 9 / 16; VY = 3.5
ch = [bgvid, veil,
      flat(30, 'veil2', 0, 0, 13.3333, 7.5, 'FFFFFF', alpha=45000),
      text(3, 'c0', L, 0.5, 11.8, 0.3, [para([run('EE499  ·  TEAM 16', 14, AMBER, spc=250)])]),
      text(4, 'c3', L, 0.85, 11.8, 0.85, [para([run('Thank you — questions?', 48, AMBER, 'Bahnschrift SemiBold')])]),
      text(5, 'c1', L, 1.85, 11.8, 0.5, [para([run('Visibility', 24, INK, 'Bahnschrift SemiBold'), run('.  ', 24, AMBER, 'Bahnschrift SemiBold'),
                                            run('Priority', 24, INK, 'Bahnschrift SemiBold'), run('.  ', 24, AMBER, 'Bahnschrift SemiBold'),
                                            run('Safety', 24, INK, 'Bahnschrift SemiBold'), run('.', 24, AMBER, 'Bahnschrift SemiBold'),
                                            run('   A need — not a luxury.', 20, SLATE, 'Segoe UI')])]),
      text(6, 'c4', L, 2.45, 11.8, 0.3, [para([run('Team 16  ·  Ali Khudhayr  ·  Mohammad Kassem  ·  Omar Baflah', 14, SLATE, 'Segoe UI')])]),
      text(8, 'sum_k', L, VY - 0.38, VW, 0.3, [para([run('IN SUMMARY', 13, SLATE, spc=250)])]),
      video(9, 'vid_summary', 'rIdSM', 'rIdSV', 'rIdSP', L, VY, VW, VH, 'Looping summary of the presentation slides'),
      text(10, 'pc_k', L + VW + 0.3, VY - 0.38, VW, 0.3, [para([run('PRIORITY CONTROL IN ACTION  ·  DS-04 / DS-05', 13, AMBER, spc=200)])]),
      video(11, 'vid_priority', 'rIdPM', 'rIdPV', 'rIdPP', L + VW + 0.3, VY, VW, VH, 'Priority control demo: lowest-priority loads are shed until demand is within the limit')]
def final_steps(t):
    return [play(t, 7, 0, 6000), play(t, 9, 0, 999000), play(t, 11, 0, 11500)] + [fadeup(t, s, 200 + i * 150) for i, s in enumerate([3, 4, 5, 6, 8, 10])]
wr('slides/slide29.xml', slide(ch, timing(final_steps, [(7, False, True), (9, True, True), (11, True, True)])))
oldbg = re.search(r'Id="(rId\d+)"[^>]*Target="\.\./media/media7\.mp4"', r29)
wr('slides/_rels/slide29.xml.rels', rels([LAYOUT, notes_rel(29), ('rId1', REL_MEDIA, '../media/media7.mp4'), ('rId2', REL_VID, '../media/media7.mp4'),
    ('rId5', REL_IMG, '../media/image64.png'), ('rIdSM', REL_MEDIA, sv), ('rIdSV', REL_VID, sv), ('rIdSP', REL_IMG, sp_),
    ('rIdPM', REL_MEDIA, '../media/media8.mp4'), ('rIdPV', REL_VID, '../media/media8.mp4'), ('rIdPP', REL_IMG, pp)]))
# ------------------------------------------------------------ slide order
order = [4, 2, 3, 5, 7, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
pres = rd('presentation.xml'); prels = rd('_rels/presentation.xml.rels')
rid_for = {int(n): r for r, n in re.findall(r'Id="(rId\d+)"[^>]*Target="slides/slide(\d+)\.xml"', prels)}
ids = dict(re.findall(r'<p:sldId id="(\d+)" r:id="(rId\d+)"/>', pres)); sid_for = {r: i for i, r in ids.items()}
lst = ''.join(f'<p:sldId id="{sid_for[rid_for[n]]}" r:id="{rid_for[n]}"/>' for n in order)
pres = re.sub(r'<p:sldIdLst>.*?</p:sldIdLst>', f'<p:sldIdLst>{lst}</p:sldIdLst>', pres, flags=re.S)
wr('presentation.xml', pres)
# ------------------------------------------------------------ page numbers: live slide-number fields, correct cached value
for pos, n in enumerate(order, 1):
    f = f'slides/slide{n}.xml'; s = rd(f)
    def fix(m):
        sp = m.group(0)
        sp = re.sub(r'<a:r><a:rPr([^>]*)>(.*?)</a:rPr><a:t>[^<]*</a:t></a:r>',
                    lambda r: f'<a:fld id="{{{str(uuid.uuid4()).upper()}}}" type="slidenum"><a:rPr lang="en-US"{re.sub(r' lang="[^"]*"', '', r.group(1))}>{r.group(2)}</a:rPr><a:t>{pos}</a:t></a:fld>', sp, count=1)
        sp = re.sub(r'(<a:fld [^>]*type="slidenum">.*?<a:t>)[^<]*(</a:t>)', lambda r: r.group(1) + str(pos) + r.group(2), sp, flags=re.S)
        return sp
    s = re.sub(r'<p:sp><p:nvSpPr><p:cNvPr id="\d+" name="pageno"/>.*?</p:sp>', fix, s, flags=re.S)
    wr(f, s)
print('built', len(order), 'slides')
# ------------------------------------------------------------ speaker notes: time budget (~8:45 total) + talking points
NOTES = {  # keyed by slide file number
 4: ('0:30', 'Opening slide: the tower spells our names and university IDs while we introduce the project — Smart Home Energy Management with Priority-Based Load Control, Report 1, advisor Dr. Fahd Hariri.'),
 2: ('0:10', 'Four parts: introduction, problem statement, objectives, design requirements.'),
 3: ('0:05', 'Why household energy needs managing.'),
 5: ('0:35', 'Homes take 47 % of Saudi electricity; about 70 % of home electricity goes to air-conditioning; above 6,000 kWh/month every extra kWh costs 67 % more (18 → 30 halalas).'),
 7: ('0:35', 'Per-appliance feedback saved a median 14 % (ACEEE, 57 studies). A dirty AC filter wastes 5–15 % and stays hidden in the total. About 53 house fires a day in KSA, mostly electrical.'),
 10: ('0:30', 'A conventional meter gives one number. Three questions it cannot answer — which appliance, which can wait, which misbehaves — map to cost, continuity and safety. Not a luxury: a need.'),
 12: ('0:25', 'Our system measures each appliance separately: voltage, current, power, energy and ON/OFF status.'),
 13: ('0:30', 'User sets priorities; when demand exceeds the limit the lowest-priority load is shed; essentials stay on.'),
 14: ('0:25', 'Abnormal operation is a supporting function: deviation from the appliance’s own baseline triggers a warning. Direct sub-metering is more reliable than whole-house estimates.'),
 15: ('0:05', 'Problem statement.'),
 16: ('0:25', 'Five problems households face today.'),
 17: ('0:20', 'The need: residential energy management with monitoring, priority control, cost management and supplied essentials.'),
 18: ('0:05', 'Objectives.'),
 19: ('0:25', 'Three higher-level objectives: economic, reliability, safety and efficiency.'),
 20: ('0:30', 'Six lower-level objectives: monitor, detect, prioritise, budget, inform, stay safe.'),
 21: ('0:05', 'Design requirements.'),
 22: ('0:30', 'DS-01 to DS-04: ±5 % accuracy, ≤ 3 s updates, ≥ 90 % abnormal detection, ≤ 1 s load control.'),
 23: ('0:30', 'DS-05 to DS-08: reconnection, cost and budget alerts, user warnings, ≤ 2 s fail-safe.'),
 24: ('0:25', 'The warning behaviour: outside 120 / 80 % of baseline for ≥ 5 s → warn within 5 s.'),
 25: ('0:20', 'Constraints C-01 to C-06: budget, single-phase scope, lab power, schedule, no appliance modification, supervised lab.'),
 26: ('0:20', 'Standards we follow for guidance: IEC 60730-1, IEC 62053-21, SBC 401, GSO low-voltage regulation.'),
 27: ('0:20', 'Assumptions behind the design.'),
 28: ('0:20', 'Five deliverables: prototype, test bench, firmware and UI, validation results, documentation.'),
 29: ('0:15', 'Close. The summary and the priority-control demo loop on their own during questions.'),
}
for pos, n in enumerate(order, 1):
    rel = rd(f'slides/_rels/slide{n}.xml.rels')
    m = re.search(r'Target="\.\./notesSlides/(notesSlide\d+\.xml)"', rel)
    if not m: continue
    f = 'notesSlides/' + m.group(1); s = rd(f)
    tm, tx = NOTES[n]
    body = f'<a:p><a:r><a:rPr lang="en-US" b="1" dirty="0"/><a:t>⏱ {tm}</a:t></a:r></a:p><a:p><a:r><a:rPr lang="en-US" dirty="0"/><a:t>{esc(tx)}</a:t></a:r></a:p>'
    s = re.sub(r'(<p:ph type="body"[^>]*/></p:nvPr></p:nvSpPr><p:spPr/><p:txBody><a:bodyPr/><a:lstStyle/>).*?(</p:txBody>)', lambda r: r.group(1) + body + r.group(2), s, count=1, flags=re.S)
    wr(f, s)
print('notes added')
