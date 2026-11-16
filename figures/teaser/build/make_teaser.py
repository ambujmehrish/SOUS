"""Single-column teaser (3.25 in). Usage: make_teaser.py <img_dir> <out.svg>"""
import base64, io, os, sys
from PIL import Image, ImageFont
IMG, OUT = sys.argv[1], sys.argv[2]
FONTDIR = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(__file__), '..', 'fonts')
W = 480                                   # 1 unit = 3.25in/480 = 0.4875 pt
INK, SUB = '#1d1d1f', '#5f6368'
MAG, TEAL, BLUE, ORG, GRID = '#B5276E', '#1C8F89', '#3A6FB0', '#E07A1F', '#A9C9EA'
FAM = "InterTT, Inter, Arial, sans-serif"
_FONTS = {(400, False): 'Inter-Regular', (500, False): 'Inter-Medium', (600, False): 'Inter-SemiBold', (700, False): 'Inter-Bold',
          (400, True): 'Inter-Italic', (500, True): 'Inter-MediumItalic', (600, True): 'Inter-SemiBoldItalic', (700, True): 'Inter-BoldItalic'}
def tw(t, size, wt=400, it=False):
    f = ImageFont.truetype(os.path.join(FONTDIR, f"Inter-{wt}-{'italic' if it else 'normal'}.ttf"), 100)
    return f.getlength(t) * size / 100
def img64(path, crop=None):
    im = Image.open(path).convert('RGB')
    if crop: im = im.crop(crop)
    b = io.BytesIO(); im.save(b, 'PNG'); return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()
s = []
add = s.append
def text(x, y, t, size, wt=400, fill=INK, anchor='start', it=False):
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{wt}" fill="{fill}" text-anchor="{anchor}"'
        f'{" font-style=\"italic\"" if it else ""}>{t}</text>')
def rect(x, y, w, h, fill='none', stroke='none', sw=1, rx=0, dash=None, op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d} opacity="{op}"/>')
def image(href, x, y, w, h, rx=4, border='#d0d3d9'):
    cid = f'c{len(s)}'
    add(f'<clipPath id="{cid}"><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}"/></clipPath>')
    add(f'<image href="{href}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" preserveAspectRatio="xMidYMid slice" clip-path="url(#{cid})"/>')
    rect(x, y, w, h, stroke=border, sw=0.9, rx=rx)
def arrow(d, color=INK, sw=1.4, dash=None, head='ah'):
    da = f' stroke-dasharray="{dash}"' if dash else ''
    add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}"{da} marker-end="url(#{head})"/>')

FONTFACE = '<style>' + ''.join(
    f"@font-face{{font-family:InterTT;font-weight:{w};font-style:{st};src:url(data:font/ttf;base64,"
    + base64.b64encode(open(os.path.join(FONTDIR, f'Inter-{w}-{st}.ttf'), 'rb').read()).decode() + ") format('truetype');}"
    for w in (400, 500, 600, 700) for st in ('normal', 'italic')) + ''.join(
    f"@font-face{{font-family:InterTT;font-weight:{w};font-style:{st};unicode-range:U+0370-03FF;src:url(data:font/ttf;base64,"
    + base64.b64encode(open(os.path.join(FONTDIR, f'InterGreek-{w}-{st}.ttf'), 'rb').read()).decode() + ") format('truetype');}"
    for w in (400, 500, 600, 700) for st in ('normal', 'italic')) + '</style>'
def dots(cx, cy, col=SUB):
    for dx in (-3.6, 0, 3.6):
        add(f'<circle cx="{cx + dx:.1f}" cy="{cy:.1f}" r="1.05" fill="{col}"/>')
body_start = len(s)
# ---------------- (a) ----------------
y = 15
text(0, y, '(a) Ask, don’t draw: masks become tokens, the MLLM points at one', 13.6, 700)
assert tw('(a) Ask, don’t draw: masks become tokens, the MLLM points at one', 13.6, 700) <= W
y += 18
text(0, y, 'Query', 12.5, 500, SUB)
text(tw('Query', 12.5, 500) + 6, y, '“Locate the seat of the bench.”', 12.5, 500, INK, it=True)
IS, GAP = 118, (W - 3 * 118) / 2
IY = y + 9
xs = [0, IS + GAP, 2 * (IS + GAP)]
image(img64(f'{IMG}/im-000.png'), xs[0], IY, IS, IS)
image(img64(f'{IMG}/im-001.png'), xs[1], IY, IS, IS)
image(img64(f'{IMG}/im-002.png'), xs[2], IY, IS, IS)
ay = IY + IS / 2
for (x0, top, bot, dash) in [(xs[0] + IS, 'SAM 3 (frozen)', 'grid + text', None), (xs[1] + IS, 'MLLM selects', 'no mask decoder', '3.5,2.5')]:
    cx = x0 + GAP / 2
    arrow(f'M{x0 + 5:.1f},{ay:.1f} L{x0 + GAP - 5:.1f},{ay:.1f}', dash=dash)
    def gwrap(t, size, wt, width):
        out, cur = [], ''
        for w_ in t.split():
            trial = (cur + ' ' + w_).strip()
            if tw(trial, size, wt) <= width or not cur: cur = trial
            else: out.append(cur); cur = w_
        return out + [cur]
    lines_top = gwrap(top, 12, 600, GAP - 4)
    for i, line in enumerate(reversed(lines_top)):
        text(cx, ay - 7 - i * 14, line, 12, 600, INK, 'middle')
    lines_bot = gwrap(bot, 11.5, 400, GAP - 4)
    for i, line in enumerate(lines_bot):
        text(cx, ay + 16 + i * 13, line, 11.5, 400, SUB, 'middle')
        assert tw(line, 11.5) <= GAP - 2, line
cy = IY + IS + 15
text(xs[1] + IS / 2, cy, '259 candidate masks', 12.5, 600, INK, 'middle')
lg = cy + 15
lw = 9 + 4 + tw('point grid', 11.5) + 12 + 9 + 4 + tw('SAM 3 text', 11.5)
lx = xs[1] + IS / 2 - lw / 2
rect(lx, lg - 8.5, 9, 9, GRID)
text(lx + 13, lg, 'point grid', 11.5, 400, SUB)
lx2 = lx + 13 + tw('point grid', 11.5) + 12
rect(lx2, lg - 8.5, 9, 9, 'none', ORG, 1.4, 1)
text(lx2 + 13, lg, 'SAM 3 text', 11.5, 400, SUB)
text(xs[2], cy, 'selected mask', 12.5, 600, MAG)

# ---------------- MLLM input sequence ----------------
BY = lg + 10
BH = 98
rect(0.6, BY, W - 1.2, BH, '#F7F8FA', '#cfd3da', 1, 8)
text(10, BY + 17, 'MLLM input sequence', 12.5, 700)
text(10 + tw('MLLM input sequence', 12.5, 700) + 7, BY + 17, 'Qwen3-VL-4B, 64.2M trainable parameters', 11.5, 400, SUB)
CH = 22; CY = BY + 52
FS = 11.5
words = 'Locate the seat of the bench.'.split()
x = 10
q0 = x
for w_ in words:
    cw = tw(w_, FS) + 9
    rect(x, CY, cw, CH, '#ffffff', '#c3c7cf', 0.9, 3.5)
    text(x + cw / 2, CY + 15, w_, FS, 400, INK, 'middle')
    x += cw + 2.5
q1 = x - 2.5
x += 7
i0 = x
for f in ('im-003.png', 'im-004.png'):
    image(img64(f'{IMG}/{f}'), x, CY, CH + 4, CH, rx=2, border='#c3c7cf'); x += CH + 6
dots(x + 3, CY + CH / 2); x += 10
i1 = x - 4
x += 6
m0 = x
scores = [0.04, 0.07, 0.53]
for n, (f, sc) in enumerate(zip(('im-005.png', 'im-006.png', 'im-007.png'), scores)):
    col = MAG if n == 2 else BLUE
    image(img64(f'{IMG}/{f}'), x, CY, CH + 4, CH, rx=3, border=col)
    rect(x, CY, CH + 4, CH, 'none', col, 1.6 if n == 2 else 1.2, 3)
    bh = max(2.5, sc / 0.53 * 22)
    rect(x + 4, CY - 4 - bh, CH - 4, bh, MAG if n == 2 else '#AEB4BD', rx=1)
    if n == 2:
        text(x - 3, CY - 10, '0.53', 11.5, 700, MAG, 'end')
        sel_bar = (x + (CH + 4) / 2, CY - 4 - bh)
    x += CH + 4
    dots(x + 5, CY + CH / 2); x += 10
m1 = x - 4
x += 6
SW = tw('<SEL>', 12, 700) + 12
SX = W - 10 - SW
assert x <= SX + 1, (x, SX)
rect(SX, CY, SW, CH, '#1F2430', rx=4)
text(SX + SW / 2, CY + 15, '&lt;SEL&gt;', 12, 700, '#ffffff', 'middle')
# braces + labels
by_ = CY + CH + 5
for (a, b, lab) in [(q0, q1, 'query'), (i0, i1, 'image'), (m0, m1, 'mask tokens (259)')]:
    add(f'<path d="M{a:.1f},{by_} L{a:.1f},{by_ + 4} L{b:.1f},{by_ + 4} L{b:.1f},{by_}" fill="none" stroke="{SUB}" stroke-width="0.9"/>')
    text((a + b) / 2, by_ + 16, lab, 11.5, 400, SUB, 'middle')
# arrows: SEL -> score bar, SEL -> selected mask
sx_ = SX + SW * 0.3
arrow(f'M{sx_:.1f},{CY - 1} C{sx_ - 4:.1f},{CY - 30} {sel_bar[0] + 22:.1f},{sel_bar[1] - 14:.1f} {sel_bar[0] + 7:.1f},{sel_bar[1] - 3:.1f}', MAG, 1.2, head='ahm')
ux = SX + SW * 0.72
arrow(f'M{ux:.1f},{CY - 1} L{ux:.1f},{IY + IS + 3}', MAG, 1.4, head='ahm')
# small down-pointer from candidates into the sequence
add(f'<path d="M{xs[1] + IS / 2 - 4:.1f},{BY - 5} L{xs[1] + IS / 2 + 4:.1f},{BY - 5} L{xs[1] + IS / 2:.1f},{BY + 0.5} Z" fill="{SUB}"/>')

# ---------------- (b) ----------------
y = BY + BH + 20
text(0, y, '(b) One read-out, three kinds of answer', 13.6, 700)
PW, PG = (W - 2 * 8) / 3, 8
CROP = [(0, 375, 344, 715), (0, 245, 344, 585), (0, 70, 344, 410)]
PH = PW * 340 / 344
panels = [('Part', '“Locate the fork of the bicycle.”', 'im-008.png', ('1 mask, IoU 0.68', MAG), 'PACO +14.5'),
          ('Several targets', '“right man and the cake”', 'im-009.png', ('2 masks, IoU 0.95', TEAL), 'gRefCOCO +20.8'),
          ('No target', '“man on left”', 'im-010.png', ('max σ 0.86 &lt; 0.90', INK), 'N-acc 89.6%')]
def wrap(t, size, width, wt=400, it=False):
    words_, lines, cur = t.split(), [], ''
    for w_ in words_:
        trial = (cur + ' ' + w_).strip()
        if tw(trial, size, wt, it) <= width or not cur: cur = trial
        else: lines.append(cur); cur = w_
    return lines + [cur]
ly = y + 18
qlines = [wrap(p[1], 11.5, PW - 2, 400, True) for p in panels]
nq = max(len(q) for q in qlines)
py = ly + 6 + nq * 13.5
for n, ((lab, q, f, (m1_, mc), m2), ql) in enumerate(zip(panels, qlines)):
    px = n * (PW + PG)
    text(px, ly, lab, 12.5, 700)
    for i, line in enumerate(ql):
        text(px, ly + 14 + i * 13.5, line, 11.5, 400, SUB, it=True)
    image(img64(f'{IMG}/{f}', CROP[n]), px, py, PW, PH)
    if n == 2:
        pw_ = tw('no target', 11.5, 600) + 30
        bx_, by2 = px + PW / 2 - pw_ / 2, py + PH - 26
        rect(bx_, by2, pw_, 19, '#ffffff', INK, 1.1, 9.5)
        add(f'<g transform="translate({bx_ + 12:.1f},{by2 + 9.5:.1f})"><circle r="4.2" fill="none" stroke="{INK}" stroke-width="1.3"/>'
            f'<line x1="-4.8" y1="4.8" x2="4.8" y2="-4.8" stroke="{INK}" stroke-width="1.3"/></g>')
        text(bx_ + 21, by2 + 13.5, 'no target', 11.5, 600)
    text(px, py + PH + 15, m1_, 12, 700, mc)
    text(px, py + PH + 29, m2, 11.5, 400, SUB)
    assert tw(m1_.replace('&lt;', '<'), 12, 700) <= PW, m1_
H = py + PH + 33
s.insert(body_start, f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-1 -1 {W + 2} {H + 2:.1f}" width="{W + 2}" height="{H + 2:.1f}" font-family="{FAM}">'
         '<defs>' + FONTFACE +
         f'<marker id="ah" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto"><path d="M0,0.8 L10,5 L0,9.2 Z" fill="{INK}"/></marker>'
         f'<marker id="ahm" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto"><path d="M0,0.8 L10,5 L0,9.2 Z" fill="{MAG}"/></marker>'
         '</defs>'
         f'<rect x="-1" y="-1" width="{W + 2}" height="{H + 2:.1f}" fill="#ffffff"/>')
add('</svg>')
open(OUT, 'w').write('\n'.join(s))
print('wrote', OUT, f'{W}x{H:.0f} units -> 3.25 x {3.25 * H / W:.2f} in')
