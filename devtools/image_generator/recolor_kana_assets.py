"""Generate a separate kana palette, preserving source dimensions and alpha.

Requires Pillow. Original exports must contain black bodies and red accents;
this is not a general-purpose recolorer for arbitrary multicolored artwork.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = ROOT / 'assets/export/font'
DEFAULT_OUTPUT = ROOT / 'assets/preview/kana-recolored'


def parse_color(value):
    if not re.fullmatch(r'#[0-9a-fA-F]{6}', value):
        raise argparse.ArgumentTypeError('Use #RRGGBB.')
    return tuple(int(value[i:i + 2], 16) for i in (1, 3, 5))


def classify(path):
    if path.name.endswith('_mark_red.png'):
        return 'partial'
    if path.name.endswith('_red.png') or path.name.startswith(('missing_mark_', 'extra_mark_')):
        return 'error'
    if 'normal' in path.parts:
        return 'normal'
    return None


def recolor(image, mode, normal, error):
    source = image.convert('RGBA')
    if mode != 'partial':
        result = Image.new('RGBA', source.size, (error if mode == 'error' else normal) + (0,))
        result.putalpha(source.getchannel('A'))
        return result
    # Red chroma separates the accent from black bodies, even at faint edges.
    pixels = []
    for r, g, b, a in source.getdata():
        color = error if r > max(g, b) * 1.7 else normal
        pixels.append((*color, a))
    result = Image.new('RGBA', source.size)
    result.putdata(pixels)
    return result


def contact_sheets(output, paths):
    pages = []
    for offset in range(0, len(paths), 80):
        batch = paths[offset:offset + 80]
        canvas = Image.new('RGB', (1440, ((len(batch) + 7) // 8) * 155), '#F7FCFE')
        draw = ImageDraw.Draw(canvas)
        for i, relative in enumerate(batch):
            x, y = (i % 8) * 180, (i // 8) * 155
            with Image.open(output / relative) as img:
                img = img.convert('RGBA')
                img.thumbnail((100, 100), Image.Resampling.LANCZOS)
                canvas.paste(img, (x + (180 - img.width) // 2, y + 5), img)
            draw.text((x + 6, y + 111), relative.parts[0], fill='#26343D')
            draw.text((x + 6, y + 129), relative.name, fill='#26343D')
        filename = f'contact-sheet-{len(pages) + 1}.png'
        canvas.save(output / filename)
        pages.append(filename)
    return pages


def example(output, normal, error):
    canvas = Image.new('RGB', (1120, 510), '#F7FCFE')
    draw = ImageDraw.Draw(canvas)
    font_path = ROOT / 'docs-myself/reference/UI/fonts/zen-maru-gothic/ZenMaruGothic-Bold.ttf'
    font = ImageFont.truetype(str(font_path), 28) if font_path.exists() else ImageFont.load_default()
    # These English labels also work without the optional local Japanese font.
    draw.text((30, 20), 'Correct / Answer / Comparison', font=font, fill=normal)
    correct = ['ga', 'xtsu', 'ko', 'u', None, 'se', 'i']
    answer = ['ka', 'tsu', 'ko', 'u', 'u', 'ze', 'i']
    result = [('wrong/ga_mark_red', None), ('wrong/xtsu_red', None),
              ('normal/ko', None), ('normal/u', None),
              ('normal/u', 'extra_mark_big'), ('wrong/se_red', None), ('normal/i', None)]
    for row in range(3):
        for col in range(7):
            if row < 2:
                name = (correct if row == 0 else answer)[col]
                if name is None:
                    continue
                relative, overlay = f'normal/{name}', None
            else:
                relative, overlay = result[col]
            with Image.open(output / f'hiragana/png/{relative}.png') as source:
                glyph = source.convert('RGBA')
                if overlay:
                    with Image.open(output / f'others/png/{overlay}.png') as mark:
                        glyph = Image.alpha_composite(glyph, mark.convert('RGBA').resize(glyph.size))
                glyph.thumbnail((110, 110), Image.Resampling.LANCZOS)
                canvas.paste(glyph, (35 + col * 150, 70 + row * 140), glyph)
    canvas.save(output / 'full-example.png')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path, default=DEFAULT_SOURCE)
    parser.add_argument('--output-dir', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--normal-color', type=parse_color, default=parse_color('#26343D'))
    parser.add_argument('--error-color', type=parse_color, default=parse_color('#AD4B55'))
    args = parser.parse_args()
    source, output = args.source_dir.resolve(), args.output_dir.resolve()
    if source == output or source in output.parents or output in source.parents:
        parser.error('Source and output must be separate, non-overlapping directories.')
    if not source.is_dir():
        parser.error('Source directory does not exist.')
    files = sorted(source.rglob('*.png'))
    if not files:
        parser.error('Source contains no PNG files.')
    output.mkdir(parents=True, exist_ok=True)
    counts, records, generated = Counter(), [], []
    for path in files:
        relative = path.relative_to(source)
        mode = classify(relative)
        if mode is None:
            counts['skipped'] += 1
            records.append({'path': str(relative), 'status': 'skipped'})
            continue
        try:
            with Image.open(path) as original:
                result = recolor(original, mode, args.normal_color, args.error_color)
                assert result.getchannel('A').tobytes() == original.convert('RGBA').getchannel('A').tobytes()
            dest = output / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            result.save(dest, optimize=True)
            counts[mode] += 1
            generated.append(relative)
            records.append({'path': str(relative), 'status': mode,
                            'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
        except (OSError, ValueError) as exc:
            counts['failed'] += 1
            records.append({'path': str(relative), 'status': 'failed', 'error': str(exc)})
    pages = contact_sheets(output, generated)
    if source == DEFAULT_SOURCE.resolve() and not counts['failed']:
        example(output, args.normal_color, args.error_color)
    report = {'source': str(source), 'normal_color': args.normal_color,
              'error_color': args.error_color, 'counts': dict(counts),
              'contact_sheets': pages, 'files': records}
    (output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'output': str(output), 'counts': dict(counts)}, indent=2))
    return 1 if counts['failed'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
