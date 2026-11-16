# Teaser, single-column version

`teaser_1col.pdf` is 3.25 in wide and fits one CVPR column:

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=\linewidth]{figures/teaser/teaser_1col.pdf}
  \caption{...}
\end{figure}
```

Images in `img/` are the ones embedded in the original double-column teaser.
Fonts are Inter (SIL Open Font License), embedded as TrueType so the PDF has no Type 3 fonts.

Rebuild:

```bash
cd figures/teaser
python3 build/make_teaser.py img teaser_1col.svg fonts
node build/render.js teaser_1col.svg teaser_1col.png teaser_1col.pdf 4
```
