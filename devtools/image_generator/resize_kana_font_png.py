import argparse
from pathlib import Path

from PIL import Image


PROJECT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE_DIR = PROJECT_DIR / "assets" / "export" / "font"
DEFAULT_OUTPUT_DIR = PROJECT_DIR / "static" / "rec" / "font"
DEFAULT_SIZE = 150


def resize_png_file(*, source_path, output_path, size):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(source_path) as image:
        resized_image = image.convert("RGBA").resize(
            (size, size),
            Image.Resampling.LANCZOS,
        )
        resized_image.save(
            output_path,
            "PNG",
            optimize=True,
        )


def resize_png_tree(*, source_dir, output_dir, size):
    png_paths = sorted(source_dir.rglob("*.png"))
    resized_count = 0

    for source_path in png_paths:
        relative_path = source_path.relative_to(source_dir)
        output_path = output_dir / relative_path
        resize_png_file(
            source_path=source_path,
            output_path=output_path,
            size=size,
        )
        resized_count += 1

    return resized_count


def main():
    parser = argparse.ArgumentParser(
        description="Resize exported kana font PNG files for web display."
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=DEFAULT_SOURCE_DIR,
        help="Source directory containing original PNG files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Output directory for resized PNG files.",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=DEFAULT_SIZE,
        help="Output image width and height in pixels.",
    )
    args = parser.parse_args()

    if not args.source_dir.exists():
        raise FileNotFoundError(f"Source directory not found: {args.source_dir}")

    resized_count = resize_png_tree(
        source_dir=args.source_dir,
        output_dir=args.output_dir,
        size=args.size,
    )

    print(f"Resized {resized_count} PNG file(s).")
    print(f"Source: {args.source_dir}")
    print(f"Output: {args.output_dir}")
    print(f"Size: {args.size}x{args.size}")


if __name__ == "__main__":
    main()
