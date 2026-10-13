# Apply the professor's notes to F_v2.
import os, re, shutil, sys, uuid
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
SRC, D = sys.argv[1], sys.argv[2]
WORK = os.path.dirname(os.path.abspath(__file__))
if os.path.exists(D): shutil.rmtree(D)
shutil.copytree(SRC, D); P = D + '/ppt/'
def rd(f): return open(P + f, encoding='utf-8').read()
def wr(f, s): open(P + f, 'w', encoding='utf-8').write(s)
def grab(s, sid):
    m = re.search(r'<p:(sp|grpSp|pic)><p:nv\w+><p:cNvPr id="%d"' % sid, s); tag = m.group(1); depth = 0
    for mm in re.finditer(r'<(/?)p:%s>' % tag, s[m.start():]):
        depth += -1 if mm.group(1) else 1
        if depth == 0: return s[m.start():m.start() + mm.end()]
def sub1(s, a, b):
    assert s.count(a) == 1, (a, s.count(a)); return s.replace(a, b)
# 1 ---- opening video: smaller, darker names (new media + matching poster)
shutil.copy(WORK + '/intro5.mp4', P + 'media/media1.mp4')
shutil.copy(WORK + '/intro5_poster.png', P + 'media/image_intro_poster.png')
r = rd('slides/_rels/slide1.xml.rels')
wr('slides/_rels/slide1.xml.rels', sub1(r, 'Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image1.png"',
                                        'Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image_intro_poster.png"'))
# 3 ---- slide 11: heavy loads overlap -> clearer wording
wr('slides/slide11.xml', sub1(rd('slides/slide11.xml'), '<a:t>Heavy loads overlap</a:t>', '<a:t>Heavy-demand loads may run at the same time</a:t>'))
# 2 ---- slide 12 becomes the formal problem statement; the 4 cards map to its 4 phrases
s = rd('slides/slide12.xml')
cards = []
for gid in (10, 15, 20, 25):
    g = grab(s, gid)
    tint = re.search(r'prst="ellipse">.*?<a:srgbClr val="([0-9A-F]{6})"', g, re.S).group(1)
    rid = re.search(r'r:embed="(rId\d+)"', g).group(1)
    descr = re.search(r'descr="([^"]*)"', g).group(1)
    cards.append((gid, tint, rid, descr))
    s = s.replace(g, '')
s = sub1(s, '<a:t>02 · PROBLEM STATEMENT — RESIDENTIAL ENERGY MANAGEMENT WITH</a:t>', '<a:t>02 · PROBLEM STATEMENT</a:t>')
s = sub1(s, '<a:t>The need</a:t>', '<a:t>Problem statement</a:t>')
H = lambda t: run(t, 22, AMBER, 'Segoe UI Semibold'); N = lambda t: run(t, 22, INK, 'Segoe UI')
stmt = [N('There is a need for a residential energy-management approach that provides '), H('① appliance-level monitoring'),
        N(', supports '), H('② priority-based control of connected loads'), N(', and helps users '),
        H('③ manage electricity consumption and cost'), N(' while '), H('④ maintaining supply to essential loads'), N('.')]
new = [shape(40, 'stmt_card', 0.75, 1.9, 11.83, 2.45, CARD),
       text(41, 'statement', 1.15, 2.15, 11.03, 2.0, [para(stmt, lnpct=118000)], anchor='ctr')]
labels = ['Appliance-level monitoring', 'Priority-based load control', 'Consumption & cost management', 'Essential loads kept supplied']
cw = (11.83 - 3 * 0.25) / 4
for i, (gid, tint, rid, descr) in enumerate(cards):
    x = 0.75 + i * (cw + 0.25); y = 4.6; b = 50 + i * 5
    new.append(group(b, f'need{i}', x, y, cw, 1.95, [
        shape(b + 1, f'need_bg{i}', x, y, cw, 1.95, CARD),
        shape(b + 2, f'need_oval{i}', x + 0.3, y + 0.3, 0.75, 0.75, tint, prst='ellipse'),
        pic(b + 3, f'need_icon{i}', rid, x + 0.465, y + 0.465, 0.42, 0.42, descr),
        text(b + 4, f'need_n{i}', x + 1.25, y + 0.42, cw - 1.45, 0.5, [para([run('①②③④'[i], 22, AMBER, 'Segoe UI Semibold')])]),
        text(b + 4 + 100, f'need_t{i}', x + 0.3, y + 1.2, cw - 0.5, 0.65, [para([run(labels[i], 16, INK)], lnpct=95000)])]))
s = sub1(s, '</p:spTree>', ''.join(new) + '</p:spTree>')
s = re.sub(r'<p:timing>.*</p:timing>', timing(fade_chain([40, 50, 55, 60, 65], 150, 220)), s, flags=re.S)
wr('slides/slide12.xml', s)
# slide 13 keeps the user's two core problems; avoid a duplicate title
wr('slides/slide13.xml', sub1(rd('slides/slide13.xml'), '<a:t>Our Problem Statement</a:t>', '<a:t>Two core problems</a:t>'))
# 4/5 ---- DS-03 and DS-06: the big number says what it measures
def ds_card(f, big_id, det_id, big_runs, det_lines, big_w=None, big_sz=None):
    s = rd(f); b = grab(s, big_id)
    rp = re.search(r'<a:rPr sz="4800"[^>]*>.*?</a:rPr>', b, re.S).group(0)
    rp_bahn = re.sub(r'typeface="[^"]*"', 'typeface="Bahnschrift SemiBold"', rp)
    if big_sz: rp_bahn = rp_bahn.replace('sz="4800"', f'sz="{big_sz}"')
    nb = re.sub(r'<a:p>.*</a:p>', '<a:p><a:pPr algn="l"/>' + ''.join(f'<a:r>{rp_bahn}<a:t>{esc(t)}</a:t></a:r>' for t in big_runs) + '</a:p>', b, flags=re.S)
    if big_w: nb = re.sub(r'<a:ext cx="\d+"', f'<a:ext cx="{E(big_w)}"', nb, count=1)
    s = s.replace(b, nb)
    d = grab(s, det_id)
    rp2 = re.search(r'<a:rPr sz="1900"[^>]*>.*?</a:rPr>', d, re.S).group(0)
    rp2s = rp2.replace('sz="1900"', 'sz="1500"').replace('val="0E1B2C"', 'val="5B6B7F"').replace('Segoe UI Semibold', 'Segoe UI')
    paras = f'<a:p><a:pPr algn="l"/><a:r>{rp2.replace("sz=\"1900\"", "sz=\"1700\"")}<a:t>{esc(det_lines[0])}</a:t></a:r></a:p>' + \
            ''.join(f'<a:p><a:pPr algn="l"/><a:r>{rp2s}<a:t>{esc(t)}</a:t></a:r></a:p>' for t in det_lines[1:])
    nd = re.sub(r'(<a:lstStyle/>).*(</p:txBody>)', lambda m: m.group(1) + paras + m.group(2), d, flags=re.S)
    if big_w:
        x0 = int(re.search(r'<a:off x="(\d+)"', b).group(1)); nx = x0 + E(big_w + 0.15); card_right = x0 + E(5.3)
        nd = re.sub(r'<a:off x="\d+" y="(\d+)"/><a:ext cx="\d+"', lambda m: f'<a:off x="{nx}" y="{m.group(1)}"/><a:ext cx="{card_right - nx}"', nd, count=1)
    wr(f, s.replace(d, nd))
ds_card('slides/slide18.xml', 26, 27, ['120 / 80 %'], ['of baseline · ≥ 5 s', '≥ 90 % detected'], big_w=2.75, big_sz=3800)
ds_card('slides/slide19.xml', 18, 19, ['±5 %'], ['cost-estimate error', 'alerts: 50 · 80 · 100 %'])
# 6 ---- final slide: priority video at true 16:9 and large; text in a left column
s = rd('slides/slide25.xml')
def move(s, sid, x, y, w, h):
    g = grab(s, sid); g2 = re.sub(r'<a:off x="-?\d+" y="-?\d+"/><a:ext cx="\d+" cy="\d+"/>', f'<a:off x="{E(x)}" y="{E(y)}"/><a:ext cx="{E(w)}" cy="{E(h)}"/>', g, count=1)
    return s.replace(g, g2)
VX, VW = 4.95, 7.63; VH = VW * 9 / 16; VY = 1.25
s = move(s, 11, VX, VY, VW, VH)                       # priority video, undistorted
s = move(s, 10, VX, VY - 0.4, VW, 0.3)                # its label
s = move(s, 3, 0.75, 0.85, 3.9, 0.3)
c3 = grab(s, 4); c3n = c3.replace('<a:t>Thank you — questions?</a:t>', '<a:t>Thank you —</a:t></a:r></a:p><a:p><a:pPr algn="l"><a:lnSpc><a:spcPct val="90000"/></a:lnSpc></a:pPr><a:r>' +
      re.search(r'<a:rPr[^>]*>.*?</a:rPr>', c3, re.S).group(0) + '<a:t>questions?</a:t>')
c3n = re.sub(r'sz="4800"', 'sz="4000"', c3n); s = s.replace(c3, c3n); s = move(s, 4, 0.75, 1.25, 3.95, 1.5)
c1 = grab(s, 5)
c1n = c1.replace('<a:t xml:space="preserve">   A need — not a luxury.</a:t>', '<a:t>A need — not a luxury.</a:t>').replace('<a:t>   A need — not a luxury.</a:t>', '<a:t>A need — not a luxury.</a:t>')
c1n = re.sub(r'(<a:r><a:rPr[^>]*sz="2000"[^>]*>(?:(?!</a:r>).)*<a:t>A need)', r'</a:p><a:p><a:pPr algn="l"/>\1', c1n, count=1, flags=re.S)
c1n = c1n.replace('sz="2000"', 'sz="1600"').replace('sz="2400"', 'sz="2000"')
s = s.replace(c1, c1n); s = move(s, 5, 0.75, 3.0, 3.95, 0.9)
c4 = grab(s, 6); c4n = c4.replace('<a:t>Team 16  ·  Ali Khudhayr  ·  Mohammad Kassem  ·  Omar Baflah</a:t>', '<a:t>Team 16</a:t>')
names = ''.join(f'<a:p><a:pPr algn="l"/><a:r>{re.search(r"<a:rPr[^>]*>.*?</a:rPr>", c4, re.S).group(0)}<a:t>{n}</a:t></a:r></a:p>' for n in ['Ali Khudhayr', 'Mohammad Kassem', 'Omar Baflah'])
c4n = c4n.replace('</a:p></p:txBody>', '</a:p>' + names + '</p:txBody>'); s = s.replace(c4, c4n); s = move(s, 6, 0.75, 4.35, 3.9, 1.3)
chips = [('≤ 1 s', 'shedding starts'), ('≥ 4 · ≥ 3', 'channels · priorities'), ('5 s', 'stable margin'), ('3 s', 'motor restarts')]
cwid = (VW - 3 * 0.2) / 4; add = ''
for i, (v, l) in enumerate(chips):
    x = VX + i * (cwid + 0.2); b = 70 + i * 4; y = VY + VH + 0.3
    add += group(b, f'chip{i}', x, y, cwid, 1.0, [shape(b + 1, f'chip_bg{i}', x, y, cwid, 1.0, CARD),
            text(b + 2, f'chip_v{i}', x + 0.18, y + 0.1, cwid - 0.3, 0.45, [para([run(v, 22, TEAL, 'Bahnschrift SemiBold')])]),
            text(b + 3, f'chip_l{i}', x + 0.18, y + 0.58, cwid - 0.3, 0.3, [para([run(l, 12, SLATE, 'Segoe UI')])])])
s = sub1(s, '</p:spTree>', add + '</p:spTree>')
wr('slides/slide25.xml', s)
# order: the formal statement closes the problem section (11 -> 13 -> 12)
pres = rd('presentation.xml')
ids = re.findall(r'<p:sldId id="\d+" r:id="rId\d+"/>', pres)
r12, r13 = ids[11], ids[12]
pres = pres.replace(r12 + r13, r13 + r12); wr('presentation.xml', pres)
# page numbers: live slide-number fields with correct cached values
prels = rd('_rels/presentation.xml.rels')
rmap = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="slides/(slide\d+)\.xml"', prels))
for pos, rid in enumerate(re.findall(r'<p:sldId id="\d+" r:id="(rId\d+)"/>', rd('presentation.xml')), 1):
    f = f'slides/{rmap[rid]}.xml'; s = rd(f)
    def fix(m):
        sp = m.group(0)
        sp = re.sub(r'<a:r><a:rPr([^>]*)>(.*?)</a:rPr><a:t>[^<]*</a:t></a:r>',
                    lambda r: f'<a:fld id="{{{str(uuid.uuid4()).upper()}}}" type="slidenum"><a:rPr lang="en-US"{re.sub(r" lang=\"[^\"]*\"", "", r.group(1))}>{r.group(2)}</a:rPr><a:t>{pos}</a:t></a:fld>', sp, count=1)
        return re.sub(r'(<a:fld [^>]*type="slidenum">.*?<a:t>)[^<]*(</a:t>)', lambda r: r.group(1) + str(pos) + r.group(2), sp, flags=re.S)
    wr(f, re.sub(r'<p:sp><p:nvSpPr><p:cNvPr id="\d+" name="pageno"/>.*?</p:sp>', fix, s, flags=re.S))
print('done')
# 7 ---- slide 8: replace the complex reproduced figure with a simple native diagram
s = rd('slides/slide8.xml'); r8 = rd('slides/_rels/slide8.xml.rels')
r8 = re.sub(r'<Relationship Id="rId3"[^>]*image25\.jpg"/>', '', r8)
ic = {'bolt': 'image32.png', 'gauge': 'image40.png', 'people': 'image55.png',
      'fridge': 'image22.png', 'ac': 'image21.png', 'heater': 'image23.png', 'washer': 'image24.png'}
r8 = r8.replace('</Relationships>', ''.join(f'<Relationship Id="rIdD_{k}" Type="{REL_IMG}" Target="../media/{v}"/>' for k, v in ic.items()) + '</Relationships>')
GREY = 'C3CEDB'
kids = []
n = [100]
def nid(): n[0] += 1; return n[0]
def arrow(x, y, w, h, prst='rightArrow'):
    return flat(nid(), 'arrow', x, y, w, h, GREY, prst=prst)
def bold_run(t, sz, col): return run(t, sz, col, 'Segoe UI Semibold')
# grid supply
gx, gy, gw, gh = 0.75, 3.3, 1.3, 1.6
kids += [shape(nid(), 'grid', gx, gy, gw, gh, CARD),
         shape(nid(), 'grid_o', gx + 0.33, gy + 0.2, 0.64, 0.64, 'FEE2E2', prst='ellipse'),
         pic(nid(), 'grid_i', 'rIdD_bolt', gx + 0.47, gy + 0.34, 0.36, 0.36, 'Grid supply'),
         text(nid(), 'grid_t', gx + 0.05, gy + 0.95, gw - 0.1, 0.6, [para([bold_run('Grid supply', 13, INK)], 'ctr'), para([run('fixed limit', 11, SLATE, 'Segoe UI')], 'ctr')])]
kids.append(arrow(2.1, 3.92, 0.3, 0.36))
# controller (dark) with user priorities above
cx, cy, cw_, ch_ = 2.45, 3.3, 1.65, 1.6
kids += [shape(nid(), 'ctrl', cx, cy, cw_, ch_, INK),
         shape(nid(), 'ctrl_o', cx + 0.5, cy + 0.2, 0.64, 0.64, '1F3147', prst='ellipse'),
         pic(nid(), 'ctrl_i', 'rIdD_gauge', cx + 0.64, cy + 0.34, 0.36, 0.36, 'Smart controller'),
         text(nid(), 'ctrl_t', cx + 0.05, cy + 0.95, cw_ - 0.1, 0.6, [para([bold_run('Smart controller', 13, 'FFFFFF')], 'ctr'), para([run('compares demand', 11, 'C3CEDB', 'Segoe UI')], 'ctr')])]
ux, uy = cx, 2.0
kids += [shape(nid(), 'user', ux, uy, cw_, 0.75, 'FEF3C7'),
         shape(nid(), 'user_o', ux + 0.12, uy + 0.12, 0.5, 0.5, AMBER, prst='ellipse'),
         pic(nid(), 'user_i', 'rIdD_people', ux + 0.2, uy + 0.2, 0.34, 0.34, 'User'),
         text(nid(), 'user_t', ux + 0.7, uy + 0.12, cw_ - 0.75, 0.5, [para([bold_run('User sets', 11, INK)]), para([bold_run('priorities', 11, INK)])], anchor='ctr'),
         arrow(cx + cw_ / 2 - 0.17, 2.82, 0.34, 0.42, prst='downArrow')]
kids.append(arrow(4.15, 3.92, 0.3, 0.36))
# appliances, highest priority first
rows = [('fridge', 'Refrigerator', 'P1 · highest', True), ('ac', 'Air conditioner', 'P2', True),
        ('heater', 'Water heater', 'P3', False), ('washer', 'Washing machine', 'P4 · lowest', False)]
ax, aw = 4.5, 2.55
for i, (k, nm, p, on) in enumerate(rows):
    y = 2.0 + i * 1.0
    kids += [shape(nid(), f'app{i}', ax, y, aw, 0.85, 'FFFFFF' if on else 'FEF2F2'),
             pic(nid(), f'app_i{i}', f'rIdD_{k}', ax + 0.12, y + 0.17, 0.5, 0.5, nm),
             text(nid(), f'app_t{i}', ax + 0.72, y + 0.12, 1.2, 0.62, [para([bold_run(nm, 11, INK if on else SLATE)]), para([run(p, 10, AMBER, 'Segoe UI Semibold')])], anchor='ctr'),
             shape(nid(), f'pill{i}', ax + aw - 0.72, y + 0.27, 0.6, 0.31, TEAL if on else RED, adj=50000),
             text(nid(), f'pill_t{i}', ax + aw - 0.72, y + 0.3, 0.6, 0.25, [para([run('ON' if on else 'SHED', 9.5, 'FFFFFF', 'Segoe UI Semibold')], 'ctr')])]
fig = grab(s, 6)
s = s.replace(fig, group(6, 'fig', 0.75, 2.0, 6.3, 3.85, kids))
s = s.replace('<a:t>Demand-side management concept. Reproduced from [4].</a:t>', '<a:t>Simplified from the demand-side management concept in [4].</a:t>')
wr('slides/slide8.xml', s); wr('slides/_rels/slide8.xml.rels', r8)
print('slide 8 redrawn')
