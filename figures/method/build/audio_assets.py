"""Synthesize illustrative audio (two same-instrument voices), render spectrogram tile and waveform envelopes."""
import numpy as np, json, sys
from PIL import Image
out = sys.argv[1]
sr = 16000; T = 4.0; t = np.arange(int(sr*T))/sr
rng = np.random.default_rng(3)
def voice(notes, vib, bright):
    y = np.zeros_like(t)
    for (st, en, f0) in notes:
        m = (t >= st) & (t < en); tt = t[m]-st
        env = np.minimum(1, tt/0.03) * (0.55+0.45*np.exp(-2.5*tt)) * np.minimum(1, (en-st-tt)/0.04)
        nz = np.convolve(rng.standard_normal(len(tt)), np.ones(400)/400, 'same'); env = env*(1+3.0*nz)
        env = env*(0.75+0.25*np.sin(2*np.pi*rng.uniform(1.5,3.0)*tt+rng.uniform(0,6))**2)
        f = f0*(1+0.006*np.sin(2*np.pi*vib*tt))
        ph = 2*np.pi*np.cumsum(f)/sr
        s = sum((bright**h)*np.sin((h+1)*ph) for h in range(8))
        y[m] += env*s
    return y
k = voice([(0.0,0.55,440),(0.6,1.1,494),(1.15,1.5,523),(1.55,2.3,587),(2.35,2.8,523),(2.85,3.95,494)], 5.5, 0.62)
j = voice([(0.0,0.95,330),(1.0,1.9,349),(1.95,2.45,392),(2.5,3.95,370)], 5.0, 0.58)
x = k + 0.8*j + 0.01*rng.standard_normal(len(t))
# spectrogram of mixture
n, hop = 1024, 128
win = np.hanning(n)
frames = np.stack([x[i:i+n]*win for i in range(0, len(x)-n, hop)])
S = np.abs(np.fft.rfft(frames, axis=1)).T[:150]  # up to ~4.7 kHz
S = 20*np.log10(S+1e-3); S = np.clip((S - (S.max()-55))/55, 0, 1)
from PIL import ImageFilter
S = S[::-1]
anchors = np.array([[0,0,4],[40,15,90],[120,30,120],[190,55,100],[245,125,80],[252,200,120],[252,253,191]])/255.
pos = np.linspace(0,1,len(anchors))
rgb = np.stack([np.interp(S, pos, anchors[:,c]) for c in range(3)], -1)
Image.fromarray((rgb*255).astype(np.uint8)).resize((360, 280), Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.8)).save(f'{out}/spec.png')
def env(y, cols=240):
    y = y/np.abs(y).max(); seg = np.array_split(y, cols)
    return [[float(s.min()), float(s.max())] for s in seg]
json.dump({'mix': env(x), 'k': env(k), 'j': env(j)}, open(f'{out}/wave.json','w'))
print('ok')
