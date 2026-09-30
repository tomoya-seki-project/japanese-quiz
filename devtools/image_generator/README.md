# Kana Background Generator

`generate_kana_bg.py` is a development helper for generating seamless kana background tiles.

Run it from the project root:

```bash
python devtools/image_generator/generate_kana_bg.py
```

If `python` is not available in the shell, use the project virtual environment or `python3`.

Generated files are written to:

```text
assets/export/background/kana_bg_output_blue/
```

## Config

The generator reads visual tuning values from `kana_bg_config.json`.

### `font_sizes`

Font size levels used when drawing kana.

The values are render-size pixels. Because the script renders at 2x scale and also exports an 800x600 logical tile, the final visual size in CSS can be smaller than these raw numbers.

Example:

```json
"font_sizes": [90, 72, 62, 40]
```

### `font_size_weights`

The appearance ratio for each matching `font_sizes` item.

The first weight belongs to the first font size, the second weight belongs to the second font size, and so on.

Example:

```json
"font_sizes": [90, 72, 62, 40],
"font_size_weights": [0.10, 0.20, 0.30, 0.40]
```

This means smaller kana appear more often than larger kana.

### `min_glyph_gap`

Extra minimum gap between different kana glyph bounding boxes.

Increasing this value makes characters less likely to touch each other. Decreasing it makes the background denser.

### `gray_levels`

Font colors used when drawing kana.

Each color is an RGBA value:

```json
[red, green, blue, alpha]
```

The current values are gray-blue tones for use on a light blue background.

### `bg_color`

Background color for the generated tile.

This is also an RGBA value:

```json
[red, green, blue, alpha]
```

### `target_counts`

How many kana characters the script tries to place in each generated tile type.

Current keys:

- `hiragana`
- `katakana`
- `mixed`

Increasing these values makes the background busier. Decreasing them gives the layout more empty space.

### `min_same_char_distance`

Minimum torus-distance between repeated appearances of the same kana.

The generated tile is seamless, so distance is calculated as if the image wraps around at the edges. For example, a kana near the left edge can still be considered close to the same kana near the right edge.

Increasing this value spreads repeated characters further apart. Decreasing it allows the same kana to appear closer together.


## Kana palette export

`recolor_kana_assets.py` requires Pillow (`python -m pip install Pillow`).

```bash
python devtools/image_generator/recolor_kana_assets.py
```

Reads `assets/export/font` and writes a separate palette to
`assets/preview/kana-recolored`. Sources are never overwritten. The original
sizes and alpha channel are preserved. Run `resize_kana_font_png.py` separately
when the palette is approved for web use.

Options: `--source-dir`, `--output-dir`, `--normal-color '#26343D'`,
`--error-color '#AD4B55'`. Source and output directories must not overlap.
Repeat runs replace matching generated files; unrelated output files are not deleted.

Normal glyphs use the normal color. Whole-glyph errors and missing/extra marks
use the error color. For `*_mark_red.png`, red source pixels are detected by
red exceeding both other channels by a factor of 1.7; other pixels retain the
normal body color. This assumes the original black/red exports, not an already
recolored source. Alpha is preserved exactly, including antialiased edges.

The output includes numbered contact sheets and `report.json` with counts,
source hashes, skipped files and failures. The default asset tree also produces
`full-example.png`: correct answer, user answer, and comparison for
`がっこうせい` / `かつこううぜい`. Extra marks overlay their kana. Unknown filenames
are skipped and reported; failed conversions cause a nonzero exit status.
