"""Method figure generator: writes a standalone SVG with embedded frames."""
import base64, json, sys, math
A = sys.argv[1]; OUT = sys.argv[2]
def b64(p): return 'data:image/png;base64,' + base64.b64encode(open(p,'rb').read()).decode()
W, H = 1000, 436
# palette
INK, SUB, LINE = '#262626', '#5f6368', '#4a4a4a'
K, J = '#D23C5A', '#7A8794'                       # clicked player k, other player j
VID, VIDL = '#7C6BD6', '#ECE8FB'                  # video tokens
KPT, KPTL = '#3F9E63', '#E2F3E8'                  # keypoint tokens
AUD, AUDL = '#E39B2D', '#FCF1DC'                  # audio tokens
FRZ, FRZS = '#E4EDF8', '#8EA8CB'                  # frozen module
TRN, TRNS = '#FDE9DA', '#E0A27A'                  # trained module
TRN2 = '#F9D2B6'
SERIF = "'Times New Roman', 'Liberation Serif', Times, serif"
s = []
def add(x): s.append(x)
def text(x, y, t, size=16, anchor='middle', weight='normal', fill=INK, style='normal', rot=None, extra=''):
    tr = f' transform="rotate({rot} {x} {y})"' if rot is not None else ''
    add(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" font-style="{style}" fill="{fill}"{tr}{extra}>{t}</text>')
def rect(x, y, w, h, fill, stroke, rx=6, sw=1.2, dash=None, op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d} opacity="{op}"/>')
def arrow(pts, color=LINE, sw=1.6, head='ah', dash=None):
    d = 'M' + ' L'.join(f'{x},{y}' for x, y in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ''
    add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round"{da} marker-end="url(#{head})"/>')
def snow(cx, cy, r=7.0, c='#3D7FD0'):
    g = [f'<g stroke="{c}" stroke-width="1.15" stroke-linecap="round" fill="none">']
    for a in range(0, 360, 60):
        ra = math.radians(a); ex, ey = cx+r*math.cos(ra), cy+r*math.sin(ra)
        g.append(f'<line x1="{cx:.2f}" y1="{cy:.2f}" x2="{ex:.2f}" y2="{ey:.2f}"/>')
        bx, by = cx+0.58*r*math.cos(ra), cy+0.58*r*math.sin(ra)
        for off in (45, -45):
            rb = ra + math.radians(off)
            g.append(f'<line x1="{bx:.2f}" y1="{by:.2f}" x2="{bx+0.36*r*math.cos(rb):.2f}" y2="{by+0.36*r*math.sin(rb):.2f}"/>')
    g.append('</g>'); add(''.join(g))
def flame(cx, cy, sc=1.0):
    add(f'<g transform="translate({cx},{cy}) scale({sc})">'
        '<path d="M0,-8 C3,-4 7,-2 6,3 C5.5,7 2.5,9 0,9 C-3.5,9 -6.5,6.5 -6,2.5 C-5.6,-0.5 -3,-1 -2.5,-4 C-1,-2.5 -0.5,-1 0,-0.5 C0.8,-3 0.6,-5.5 0,-8 Z" fill="url(#fl)"/>'
        '<path d="M0,1.5 C1.8,3 2.8,4.5 2.4,6.2 C2,7.6 1,8.2 0,8.2 C-1.4,8.2 -2.6,7.2 -2.4,5.6 C-2.2,4.2 -0.8,3.5 0,1.5 Z" fill="#FFD25A"/></g>')
def wave(x, y, w, h, env, color, sw=0.9):
    n = len(env); dx = w/n; mid = y + h/2
    top = ' L'.join(f'{x+i*dx:.2f},{mid - mx*h/2*0.92:.2f}' for i, (mn, mx) in enumerate(env))
    bot = ' L'.join(f'{x+i*dx:.2f},{mid - mn*h/2*0.92:.2f}' for i, (mn, mx) in reversed(list(enumerate(env))))
    add(f'<path d="M{top} L{bot} Z" fill="{color}" stroke="{color}" stroke-width="{sw*0.4}"/>')
def person(cx, cy, body, sc=1.0, note=None):
    add(f'<g transform="translate({cx},{cy}) scale({sc})"><circle cx="0" cy="-7" r="4.6" fill="{body}"/>'
        f'<path d="M-8,8 C-8,0 -4.5,-1.5 0,-1.5 C4.5,-1.5 8,0 8,8 Z" fill="{body}"/></g>')
    if note:
        add(f'<g transform="translate({cx+9*sc},{cy-6*sc}) scale({sc})"><ellipse cx="0" cy="4" rx="2.6" ry="2" fill="{note}" transform="rotate(-20 0 4)"/>'
            f'<line x1="2.3" y1="3.4" x2="2.3" y2="-5" stroke="{note}" stroke-width="1.3"/>'
            f'<path d="M2.3,-5 C4.5,-4 5.5,-2.5 5,-0.5" fill="none" stroke="{note}" stroke-width="1.3"/></g>')


from PIL import ImageFont
_F = {('n','n'):'LiberationSerif-Regular',('b','n'):'LiberationSerif-Bold',('n','i'):'LiberationSerif-Italic',('b','i'):'LiberationSerif-BoldItalic'}
def tw(t, size, bold=False, ital=False):
    f = ImageFont.truetype(f"/usr/share/fonts/truetype/liberation/{_F[('b' if bold else 'n','i' if ital else 'n')]}.ttf", 100)
    return f.getlength(t)*size/100
def ibox(x, y, h, label, kind, size=15, minw=0):
    w = max(minw, 9 + 13 + 5 + tw(label, size, True) + 9)
    fill, st = (FRZ, FRZS) if kind == 'frz' else ((TRN, TRNS) if kind == 'trn' else ('#f3f3f3', '#a0a0a0'))
    rect(x, y, w, h, fill, st)
    if kind == 'frz': snow(x+9+6.5, y+h/2)
    elif kind == 'trn': flame(x+9+6.5, y+h/2, 0.9)
    tx = x+9+13+5 if kind in ('frz','trn') else x+w/2-tw(label,size,True)/2
    text(tx, y+h/2+size*0.34, label, size, anchor='start', weight='bold')
    return w
HALO = ''
def plate(cx, y, label, size):
    w = tw(label, size) + 6
    add(f'<rect x="{cx-w/2:.1f}" y="{y-size*0.78:.1f}" width="{w:.1f}" height="{size*1.05:.1f}" fill="#ffffff"/>')

add(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{SERIF}">')
add('<defs>'
    f'<marker id="ah" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0.8 L10,5 L0,9.2 Z" fill="{LINE}"/></marker>'
    f'<marker id="ahg" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4.2" markerHeight="4.2" orient="auto"><path d="M0,0.8 L10,5 L0,9.2 Z" fill="#1E7A43"/></marker>'
    '<linearGradient id="fl" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#E8461E"/><stop offset="1" stop-color="#F7922A"/></linearGradient>'
    '</defs>')
add(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>')
wav = json.load(open(f'{A}/wave.json'))
frame, crop, spec = b64(f'{A}/frame.png'), b64(f'{A}/crop_k.png'), b64(f'{A}/spec.png')
ROW1, ROW2, ROWA = 46, 132, 248          # video-token row, keypoint row, audio row (centre lines)

# shared clock gridlines
TX0, VSTEP = 606, 24
SPAN = 4*VSTEP+16; TC = TX0+SPAN/2
ASTEP = VSTEP/2*25/86.13; NAUD = int(SPAN/ASTEP)
for i in range(5):
    gx = TX0 + 8 + i*VSTEP
    add(f'<line x1="{gx}" y1="30" x2="{gx}" y2="{ROWA+14}" stroke="#bcc1c8" stroke-width="0.9" stroke-dasharray="2.5,2.5"/>')
text(TC, 20, 'shared clock (RoPE, 10 ms)', 14, fill=SUB, style='italic')

# ---------- input video + click ----------
FX, FY, FW = 12, 34, 190
FH = FW*320/862
text(FX+FW/2, 24, 'Input video', 17, weight='bold')
add(f'<clipPath id="cf"><rect x="{FX}" y="{FY}" width="{FW}" height="{FH:.2f}" rx="3"/></clipPath>')
add(f'<image href="{frame}" x="{FX}" y="{FY}" width="{FW}" height="{FH:.2f}" preserveAspectRatio="none" clip-path="url(#cf)"/>')
rect(FX, FY, FW, FH, 'none', '#3a3a3a', rx=3, sw=1)
fs = FW/862
fx = lambda px: FX + px*fs; fy = lambda py: FY + py*fs
bx0, by0, bs = fx(174), fy(94), 226*fs
add(f'<rect x="{bx0:.2f}" y="{by0:.2f}" width="{bs:.2f}" height="{FY+FH-by0-0.8:.2f}" fill="none" stroke="{K}" stroke-width="1.8"/>')
add(f'<rect x="{bx0-0.9:.2f}" y="{by0-11:.2f}" width="13" height="11" fill="{K}"/>')
text(bx0+5.6, by0-2.4, 'k', 11.5, fill='#fff', style='italic', weight='bold')
jx, jy = fx(570), fy(118)
add(f'<rect x="{jx-6.5:.2f}" y="{jy-13:.2f}" width="13" height="11" rx="2" fill="{J}"/>')
text(jx, jy-4.4, 'j', 11.5, fill='#fff', style='italic', weight='bold')
cx, cy = fx(300), fy(225)
add(f'<g transform="translate({cx:.2f},{cy:.2f}) scale(0.85)"><circle cx="0" cy="0" r="6" fill="none" stroke="#fff" stroke-width="1.6"/>'
    f'<path d="M0,0 L0,15 L3.6,11.4 L6.4,17.6 L8.6,16.6 L5.8,10.4 L10.8,10.4 Z" fill="#fff" stroke="#111" stroke-width="1.1" stroke-linejoin="round"/></g>')
text(FX+FW/2, FY+FH+17, f'Click on player <tspan font-style="italic" fill="{K}" font-weight="bold">k</tspan>', 15.5, fill=SUB)

# ---------- SAM 2.1 -> crops ----------
mid = FY + FH/2
sx = FX+FW+16
arrow([(FX+FW+1, mid), (sx-2, mid)])
sw_ = ibox(sx, mid-18, 36, 'SAM 2.1', 'frz')
text(sx+sw_/2, mid+34, 'track', 14, fill=SUB, style='italic')
CS = 58; cx0 = sx+sw_+15
arrow([(sx+sw_+1, mid), (cx0-2, mid)])
for (ox, oy, op) in [(14, -14, 0.5), (7, -7, 0.75), (0, 0, 1.0)]:
    x0, y0 = cx0+ox, mid-CS/2+6+oy
    add(f'<image href="{crop}" x="{x0}" y="{y0}" width="{CS}" height="{CS}" opacity="{op}"/>')
    add(f'<rect x="{x0}" y="{y0}" width="{CS}" height="{CS}" fill="none" stroke="{K}" stroke-width="1.3"/>')
text(cx0+CS/2+7, mid+CS/2+24, 'Player crops', 15.5, fill=SUB)

# ---------- frozen encoders ----------
ex = cx0+CS+14+15
jn = cx0+CS+14+6
arrow([(cx0+CS+15, mid), (jn, mid), (jn, ROW1), (ex-2, ROW1)])
arrow([(jn, mid), (jn, ROW2), (ex-2, ROW2)])
vw = ibox(ex, ROW1-18, 36, 'V-JEPA 2', 'frz')
rw = ibox(ex, ROW2-18, 36, 'RTMW', 'frz')
KX, KS = ex+rw+10, 60
arrow([(ex+rw+1, ROW2), (KX-2, ROW2)], sw=1.3)
add(f'<clipPath id="ck"><rect x="{KX}" y="{ROW2-KS/2}" width="{KS}" height="{KS}" rx="3"/></clipPath>')
add(f'<image href="{crop}" x="{KX}" y="{ROW2-KS/2}" width="{KS}" height="{KS}" clip-path="url(#ck)" opacity="0.85"/>')
rect(KX, ROW2-KS/2, KS, KS, 'none', '#7d7d7d', rx=3, sw=0.9)
sc = KS/452
kp = lambda px, py: (KX+px*sc, ROW2-KS/2+py*sc)
bones = [((185,135),(178,195)),((178,195),(120,225)),((178,195),(240,215)),((120,225),(98,295)),((98,295),(212,290)),
         ((240,215),(268,300)),((268,300),(350,232)),((120,225),(128,368)),((240,215),(232,368)),((128,368),(232,368))]
for (a, b) in bones:
    (x1, y1), (x2, y2) = kp(*a), kp(*b)
    add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#ffffff" stroke-width="1.1"/>')
for p in [(185,135),(172,120),(198,120),(178,195),(120,225),(240,215),(98,295),(212,290),(268,300),(350,232),(128,368),(232,368),
          (222,282),(228,296),(204,298),(360,222),(372,232),(364,240)]:
    x1, y1 = kp(*p)
    add(f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="1.6" fill="{KPT}" stroke="#fff" stroke-width="0.5"/>')
for (p, v) in [((212,290),(78,-70)),((98,295),(44,-40)),((350,232),(-40,16))]:
    x1, y1 = kp(*p); x2, y2 = kp(p[0]+v[0], p[1]+v[1])
    add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#1E7A43" stroke-width="1.7" marker-end="url(#ahg)"/>')
text(KX+KS/2, ROW2+KS/2+16, 'velocities', 14, fill=SUB, style='italic')
assert KX+KS < TX0-14, (KX+KS, TX0)

# ---------- token rows ----------
arrow([(ex+vw+1, ROW1), (TX0-5, ROW1)])
arrow([(KX+KS+1, ROW2), (TX0-5, ROW2)])
for i in range(5):
    gx = TX0 + i*VSTEP; gy = ROW1-8
    for r in range(4):
        for c in range(4):
            sh = 0.55 + 0.45*((r*4+c+i*3) % 7)/6
            add(f'<rect x="{gx+c*4:.1f}" y="{gy+r*4:.1f}" width="4" height="4" fill="{VID}" opacity="{sh:.2f}" stroke="#fff" stroke-width="0.4"/>')
plate(TC, ROW1+28, 'Video tokens', 15.5); text(TC, ROW1+28, 'Video tokens', 15.5, fill=SUB, extra=HALO)
for i in range(10):
    kx = TX0 + 5.5 + i*VSTEP/2
    add(f'<rect x="{kx:.1f}" y="{ROW2-11}" width="5" height="22" rx="1.5" fill="{KPT}" opacity="{0.6+0.4*((i*5)%7)/6:.2f}"/>')
plate(TC, ROW2+29, 'Keypoint tokens', 15.5); text(TC, ROW2+29, 'Keypoint tokens', 15.5, fill=SUB, extra=HALO)
BX = TX0+SPAN+6
add(f'<path d="M{BX},{ROW1-12} C{BX+6},{ROW1-12} {BX+6},{ROW1-8} {BX+6},{ROW1-2} L{BX+6},{(ROW1+ROW2)/2-6} C{BX+6},{(ROW1+ROW2)/2} {BX+10},{(ROW1+ROW2)/2} {BX+13},{(ROW1+ROW2)/2} '
    f'C{BX+10},{(ROW1+ROW2)/2} {BX+6},{(ROW1+ROW2)/2} {BX+6},{(ROW1+ROW2)/2+6} L{BX+6},{ROW2+2} C{BX+6},{ROW2+8} {BX+6},{ROW2+12} {BX},{ROW2+12}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
ZY = (ROW1+ROW2)/2
text(BX+26, ZY+6, '<tspan font-style="italic">Z</tspan><tspan font-style="italic" font-size="12.5" dy="4">k</tspan>', 19)
for i in range(NAUD):
    ax = TX0 + 0.6 + i*ASTEP
    add(f'<rect x="{ax:.1f}" y="{ROWA-10}" width="2.4" height="20" rx="0.8" fill="{AUD}" opacity="{0.55+0.45*((i*3)%8)/7:.2f}"/>')
plate(TC, ROWA+29, 'Audio tokens H', 15.5); text(TC, ROWA+29, 'Audio tokens <tspan font-style="italic">H</tspan>', 15.5, fill=SUB, extra=HALO)

# ---------- audio input path ----------
text(FX+FW/2, ROWA-36, 'Mixture <tspan font-style="italic">x</tspan>', 17, weight='bold')
rect(FX, ROWA-25, FW, 50, '#fafafa', '#9a9a9a', rx=3, sw=0.9)
wave(FX+4, ROWA-22, FW-8, 44, wav['mix'], '#5a5a5a')
arrow([(FX+FW+1, ROWA), (sx-2, ROWA)])
stw = ibox(sx, ROWA-18, 36, 'STFT', 'op', minw=56)
SPX = cx0
arrow([(sx+stw+1, ROWA), (SPX-2, ROWA)])
add(f'<clipPath id="csp"><rect x="{SPX}" y="{ROWA-25}" width="66" height="50" rx="3"/></clipPath>')
add(f'<image href="{spec}" x="{SPX}" y="{ROWA-25}" width="66" height="50" preserveAspectRatio="none" clip-path="url(#csp)"/>')
rect(SPX, ROWA-25, 66, 50, 'none', '#3a3a3a', rx=3, sw=0.9)
text(SPX+33, ROWA+44, '<tspan font-style="italic">X</tspan>', 17)
arrow([(SPX+67, ROWA), (ex-2, ROWA)])
bw = ibox(ex, ROWA-18, 36, 'Band split', 'trn')
arrow([(ex+bw+1, ROWA), (TX0-5, ROWA)])

# ---------- separator trunk ----------
TL, TR, TT, TB = 722, 874, 150, 344
rect(TL, TT, TR-TL, TB-TT, '#FFFBF7', '#C98B62', rx=10, sw=1.3, dash='5,3')
ttl = 'Separator trunk'
tww = 16 + tw(ttl, 15.5, True)
flame(TL+(TR-TL)/2-tww/2+6, TB-16, 0.95)
text(TL+(TR-TL)/2-tww/2+16, TB-11, ttl, 15.5, anchor='start', weight='bold')
text(TR-8, TT+18, '× 12', 15.5, anchor='end', fill=SUB, style='italic')
IT, IH = 176, 144
inner = [(734, 30, 'Time Transformer', TRN, False), (780, 34, 'Cross-Attention', TRN2, True), (830, 30, 'Band Transformer', TRN, False)]
for (x0, w0, lab, fill, b) in inner:
    rect(x0, IT, w0, IH, fill, TRNS, rx=5)
    text(x0+w0/2, IT+IH/2, lab, 15, rot=-90, extra=' dominant-baseline="central"', weight='bold' if b else 'normal')
assert IT+IH/2 == ROWA
assert tww < TR-TL-16, tww
arrow([(TX0+SPAN+3, ROWA), (732, ROWA)])
arrow([(765, ROWA), (778, ROWA)])
text(771.5, ROWA-8, '<tspan font-style="italic">Q</tspan>', 13.5, fill=SUB)
arrow([(815, ROWA), (828, ROWA)])
arrow([(BX+44, ZY), (797, ZY), (797, IT-2)])
text(805, 128, '<tspan font-style="italic">K</tspan>, <tspan font-style="italic">V</tspan>', 14, anchor='start', fill=SUB)

# ---------- mask head + output ----------
MX = TR+8
arrow([(861, ROWA), (MX-2, ROWA)])
mw = ibox(MX, ROWA-18, 36, 'Mask head', 'trn')
OC = MX+mw/2
OT, OHh = 150, 40
arrow([(OC, ROWA-19), (OC, OT+OHh+2)])
_xw = tw('X', 14, ital=True); _cc = OC-6-_xw-7
text(OC-6, 209, '<tspan font-style="italic">X</tspan>', 14, anchor='end', fill=SUB)
add(f'<circle cx="{_cc:.1f}" cy="204.6" r="3.6" fill="none" stroke="{SUB}" stroke-width="0.9"/><circle cx="{_cc:.1f}" cy="204.6" r="0.95" fill="{SUB}"/>')
text(_cc-6.5, 209, '<tspan font-style="italic">M</tspan>', 14, anchor='end', fill=SUB)
text(OC-6, 225, 'iSTFT', 14, anchor='end', fill=SUB)
rect(MX, OT, mw, OHh, '#FFF6F8', K, rx=3, sw=1.1)
wave(MX+3, OT+3, mw-6, OHh-6, wav['k'], K)
add(f'<text x="{OC}" y="{OT-9}" font-size="19" text-anchor="middle" fill="{K}"><tspan font-style="italic">ŝ</tspan><tspan font-style="italic" font-size="12.5" dy="4">k</tspan></text>')
assert MX+mw <= 989, MX+mw

# ---------- training strip ----------
SY = 354
rect(12, SY, 976, 76, '#F7F6FB', '#C9C3DF', rx=10, sw=1.1)
text(26, SY+26, 'Training', 17, anchor='start', weight='bold')
text(26, SY+46, 'synthetic mixtures', 15, anchor='start', fill=SUB)
text(26, SY+64, 'of solo videos', 15, anchor='start', fill=SUB)
stages = [('Different instrument', '0–4k'), ('Same instrument', '4k–8k'), ('Same performer', '8k–12k'), ('All mixed', '12k+')]
CX, CW, GAP = 160, 132, 16
NA, NB = '#C97A1E', '#3D7FD0'
for i, (lab, st) in enumerate(stages):
    x0 = CX + i*(CW+GAP); y0 = SY+9
    rect(x0, y0, CW, 58, '#ffffff', '#cfcbe0', rx=7, sw=1)
    text(x0+CW/2, y0+13, f'steps {st}', 12.5, fill='#8a8a8a', style='italic')
    py = y0+31
    if i < 3:
        person(x0+CW/2-26, py, K, note=NA); text(x0+CW/2, py+4, '+', 15, fill=SUB)
        person(x0+CW/2+18, py, [J, J, K][i], note=[NB, NA, NA][i])
        if i == 2:
            add(f'<g transform="translate({x0+CW/2+42},{py-1})"><circle r="5.2" fill="#fff" stroke="{SUB}" stroke-width="1"/>'
                f'<path d="M0,-3 L0,0 L2.4,1.4" fill="none" stroke="{SUB}" stroke-width="1"/></g>')
    else:
        person(x0+26, py, K, note=NA); text(x0+45, py+4, '+', 15, fill=SUB)
        for n, (col, nt) in enumerate([(J, NA), ('#A9B4BF', NB), ('#A9B4BF', '#3F9E63'), ('#A9B4BF', '#8A63D2')]):
            person(x0+60+n*19, py+1, col, sc=0.74, note=nt)
    text(x0+CW/2, y0+52, lab, 15)
    if i < 3:
        arrow([(x0+CW+1, y0+29), (x0+CW+GAP-2, y0+29)], sw=1.3)
mx0 = CX + 4*(CW+GAP) + 4
rect(mx0, SY+9, 104, 58, '#ffffff', '#cfcbe0', rx=7, sw=1)
person(mx0+32, SY+40, K, note=NA)
add(f'<g transform="translate({mx0+72},{SY+40}) scale(-1,1)" opacity="0.55"><circle cx="0" cy="-7" r="4.6" fill="{K}"/><path d="M-8,8 C-8,0 -4.5,-1.5 0,-1.5 C4.5,-1.5 8,0 8,8 Z" fill="{K}"/>'
    f'<g transform="translate(9,-6)"><ellipse cx="0" cy="4" rx="2.6" ry="2" fill="{NA}" transform="rotate(-20 0 4)"/><line x1="2.3" y1="3.4" x2="2.3" y2="-5" stroke="{NA}" stroke-width="1.3"/><path d="M2.3,-5 C4.5,-4 5.5,-2.5 5,-0.5" fill="none" stroke="{NA}" stroke-width="1.3"/></g></g>')
add(f'<line x1="{mx0+52}" y1="{SY+20}" x2="{mx0+52}" y2="{SY+48}" stroke="{SUB}" stroke-width="0.9" stroke-dasharray="2,2"/>')
text(mx0+52, SY+61, 'Mirror, <tspan font-style="italic">p</tspan> = 0.5', 15)
lx = mx0 + 104 + 14
flame(lx+8, SY+27, 0.95); text(lx+20, SY+32, 'Trained', 15, anchor='start')
snow(lx+8, SY+53); text(lx+20, SY+58, 'Frozen', 15, anchor='start')
assert lx+20+tw('Trained', 15) < 986, lx
add('</svg>')
open(OUT, 'w').write('\n'.join(s))
print('wrote', OUT, 'encoders at', ex, 'kp end', KX+KS)
