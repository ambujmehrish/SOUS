# Method figure (Fig. 1)

`method.pdf` is the vector version to include in the paper:

```latex
\includegraphics[width=\textwidth]{figures/method/method.pdf}
```

The frame comes from the URMP project page gallery (the two-violin "Sonata" duet). It is a small thumbnail.
For the camera-ready version, replace `assets/frame.png` (862x320) and `assets/crop_k.png` (452x452, the square box around player k) with full-resolution frames from your URMP copy, then rebuild:

```bash
cd figures/method
python3 build/make_figure.py assets method.svg
node build/render.js method.svg method.png method.pdf 4
```

`build/audio_assets.py` regenerates the illustrative waveforms and spectrogram. They are synthetic and only for illustration.
