import json
import os
import random
from collections import defaultdict
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# =========================================================
# CONFIG
# =========================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_DIR / "assets" / "export" / "background" / "kana_bg_output_blue"
CONFIG_PATH = SCRIPT_DIR / "kana_bg_config.json"

# Final logical tile size for CSS / layout
LOGICAL_W = 800
LOGICAL_H = 600

# Render at 2x for better quality, then also export 800x600 copy
SCALE = 2
TILE_W = LOGICAL_W * SCALE
TILE_H = LOGICAL_H * SCALE

# Try auto-detect font. If needed, set FORCE_FONT_PATH manually.
FORCE_FONT_PATH = None
# Example:
# FORCE_FONT_PATH = r"C:\Windows\Fonts\YuGothB.ttc"

SEED = 42

def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as config_file:
        return json.load(config_file)


CONFIG = load_config(CONFIG_PATH)

# Font size levels used during high-resolution rendering.
FONT_SIZES = CONFIG["font_sizes"]

# Relative selection weights for each font size.
FONT_SIZE_WEIGHTS = CONFIG["font_size_weights"]

MIN_GLYPH_GAP = CONFIG["min_glyph_gap"]

GRAY_LEVELS = [tuple(color) for color in CONFIG["gray_levels"]]

# Tile background color.
BG_COLOR = tuple(CONFIG["bg_color"])

# Target number of glyphs for each generated tile.
TARGET_COUNTS = CONFIG["target_counts"]

# Minimum wrapped distance between repeated instances of the same character.
MIN_SAME_CHAR_DISTANCE = CONFIG["min_same_char_distance"]  # Render pixels.

# Maximum placement attempts per target glyph.
MAX_ATTEMPT_MULTIPLIER = 120


# =========================================================
# CHARACTER SETS
# Only legal kana, no strange symbols, no prolonged mark, no punctuation
# =========================================================

HIRAGANA = list(
    "あいうえお"
    "かきくけこ"
    "さしすせそ"
    "たちつてと"
    "なにぬねの"
    "はひふへほ"
    "まみむめも"
    "やゆよ"
    "らりるれろ"
    "わをん"
    "がぎぐげご"
    "ざじずぜぞ"
    "だぢづでど"
    "ばびぶべぼ"
    "ぱぴぷぺぽ"
)

KATAKANA = list(
    "アイウエオ"
    "カキクケコ"
    "サシスセソ"
    "タチツテト"
    "ナニヌネノ"
    "ハヒフヘホ"
    "マミムメモ"
    "ヤユヨ"
    "ラリルレロ"
    "ワヲン"
    "ガギグゲゴ"
    "ザジズゼゾ"
    "ダヂヅデド"
    "バビブベボ"
    "パピプペポ"
)


# =========================================================
# HELPERS
# =========================================================

def find_font_path(force_path=None):
    if force_path and os.path.exists(force_path):
        return force_path

    candidates = [
        # Windows
        r"C:\Windows\Fonts\YuGothB.ttc",
        r"C:\Windows\Fonts\YuGothM.ttc",
        r"C:\Windows\Fonts\meiryo.ttc",
        r"C:\Windows\Fonts\msgothic.ttc",
        r"C:\Windows\Fonts\msyh.ttc",
        # WSL access to Windows fonts
        "/mnt/c/Windows/Fonts/YuGothB.ttc",
        "/mnt/c/Windows/Fonts/YuGothM.ttc",
        "/mnt/c/Windows/Fonts/meiryo.ttc",
        # macOS
        "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        "/System/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc",
        # Linux
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansJP-Regular.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]

    for path in candidates:
        if os.path.exists(path):
            return path

    raise FileNotFoundError(
        "No suitable Japanese font found.\n"
        "Please set FORCE_FONT_PATH manually, e.g.\n"
        r'FORCE_FONT_PATH = r"C:\Windows\Fonts\YuGothB.ttc"'
    )

def torus_axis_distance(a, b, total_length):
    # Calculate the shortest distance along one axis on a wrapping canvas.
    # For example, on a 1600px-wide tile, x=10 and x=1590 are only 20px apart.
    distance = abs(a - b)
    return min(distance, total_length - distance)


def glyphs_overlap(
        x1,
        y1,
        width1,
        height1,
        x2,
        y2,
        width2,
        height2,
        canvas_width,
        canvas_height,
        gap,
    ):
    # Use axis-aligned bounding boxes to detect overlap between two glyphs.
    # The gap value adds extra spacing around each glyph pair.

    dx = torus_axis_distance(x1, x2, canvas_width)
    dy = torus_axis_distance(y1, y2, canvas_height)

    required_x_distance = (width1 + width2) / 2 + gap
    required_y_distance = (height1 + height2) / 2 + gap

    return (
        dx < required_x_distance
        and dy < required_y_distance
)

def torus_distance(x1, y1, x2, y2, w, h):
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    dx = min(dx, w - dx)
    dy = min(dy, h - dy)
    return (dx * dx + dy * dy) ** 0.5


def too_close_same_char(ch, x, y, placed_by_char, min_dist, w, h):
    for px, py in placed_by_char[ch]:
        if torus_distance(x, y, px, py, w, h) < min_dist:
            return True
    return False


def build_glyph_image(ch, font, rgba):
    bbox = font.getbbox(ch)
    gw = bbox[2] - bbox[0]
    gh = bbox[3] - bbox[1]

    img = Image.new("RGBA", (gw, gh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((-bbox[0], -bbox[1]), ch, font=font, fill=rgba)
    return img


def paste_seamless(canvas, glyph_img, center_x, center_y, tile_w, tile_h):
    gw, gh = glyph_img.size
    left = int(round(center_x - gw / 2))
    top = int(round(center_y - gh / 2))

    # Draw on the base tile and neighboring wrapped positions for seamless edges.
    for ox in (-tile_w, 0, tile_w):
        for oy in (-tile_h, 0, tile_h):
            canvas.alpha_composite(glyph_img, (left + ox, top + oy))


def save_preview(tile_img, out_path):
    # Build a 2x2 preview from the logical-size tile to verify seamless tiling.
    preview = Image.new("RGBA", (LOGICAL_W * 2, LOGICAL_H * 2), BG_COLOR)
    preview.alpha_composite(tile_img, (0, 0))
    preview.alpha_composite(tile_img, (LOGICAL_W, 0))
    preview.alpha_composite(tile_img, (0, LOGICAL_H))
    preview.alpha_composite(tile_img, (LOGICAL_W, LOGICAL_H))
    preview.convert("RGB").save(out_path)


def generate_tile(name, charset, font_path, seed, target_count):
    rng = random.Random(seed)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Cache font objects by size to avoid rebuilding them for every glyph.
    font_cache = {size: ImageFont.truetype(font_path, size=size) for size in FONT_SIZES}

    # Main high-resolution tile canvas.
    canvas = Image.new("RGBA", (TILE_W, TILE_H), BG_COLOR)

    placed_by_char = defaultdict(list)
    placed_items = []
    glyph_cache = {}

    placed = 0
    attempts = 0
    max_attempts = target_count * MAX_ATTEMPT_MULTIPLIER

    while placed < target_count and attempts < max_attempts:
        attempts += 1

        ch = rng.choice(charset)
        size = rng.choices(
            FONT_SIZES,
            weights=FONT_SIZE_WEIGHTS,
            k=1,
        )[0]
        gray = rng.choice(GRAY_LEVELS)

        cache_key = (ch, size, gray)

        if cache_key not in glyph_cache:
            glyph_cache[cache_key] = build_glyph_image(
                ch,
                font_cache[size],
                gray,
            )

        glyph_img = glyph_cache[cache_key]
        glyph_width, glyph_height = glyph_img.size

        x = rng.uniform(0, TILE_W)
        y = rng.uniform(0, TILE_H)

        # -----------------------------------------------------
        # 1. Avoid placing the same character too close to a previous instance.
        # -----------------------------------------------------

        if too_close_same_char(
            ch,
            x,
            y,
            placed_by_char,
            MIN_SAME_CHAR_DISTANCE,
            TILE_W,
            TILE_H,
        ):
            continue

        # -----------------------------------------------------
        # 2. Avoid visual collisions between any two glyphs.
        # -----------------------------------------------------

        has_collision = False

        for item in placed_items:
            if glyphs_overlap(
                x1=x,
                y1=y,
                width1=glyph_width,
                height1=glyph_height,

                x2=item["x"],
                y2=item["y"],
                width2=item["width"],
                height2=item["height"],

                canvas_width=TILE_W,
                canvas_height=TILE_H,
                gap=MIN_GLYPH_GAP,
            ):
                has_collision = True
                break

        if has_collision:
            continue

        # -----------------------------------------------------
        # 3. Place the glyph once all spacing checks pass.
        # -----------------------------------------------------

        paste_seamless(
            canvas,
            glyph_img,
            x,
            y,
            TILE_W,
            TILE_H,
        )

        placed_items.append({
            "char": ch,
            "x": x,
            "y": y,
            "width": glyph_width,
            "height": glyph_height,
        })

        placed_by_char[ch].append((x, y))

        placed += 1

    print(f"[{name}] placed {placed}/{target_count} chars after {attempts} attempts")

    # Save hi-res tile
    hi_res_path = os.path.join(OUTPUT_DIR, f"{name}_tile_1600x1200.png")
    canvas.convert("RGB").save(hi_res_path)

    # Save logical-size tile
    tile_800 = canvas.resize((LOGICAL_W, LOGICAL_H), resample=Image.Resampling.LANCZOS)
    tile_800_path = os.path.join(OUTPUT_DIR, f"{name}_tile_800x600.png")
    tile_800.convert("RGB").save(tile_800_path)

    # Save 2x2 preview for seamless checking
    preview_path = os.path.join(OUTPUT_DIR, f"{name}_preview_1600x1200.png")
    save_preview(tile_800, preview_path)

    return hi_res_path, tile_800_path, preview_path


def main():
    font_path = find_font_path(FORCE_FONT_PATH)
    print("Using font:", font_path)

    jobs = [
        ("katakana", KATAKANA, SEED + 1, TARGET_COUNTS["katakana"]),
        ("hiragana", HIRAGANA, SEED + 2, TARGET_COUNTS["hiragana"]),
        ("mixed", HIRAGANA + KATAKANA, SEED + 3, TARGET_COUNTS["mixed"]),
    ]

    results = []
    for name, charset, seed, target_count in jobs:
        result = generate_tile(name, charset, font_path, seed, target_count)
        results.append((name, result))

    print("\nDone. Files saved to:", os.path.abspath(OUTPUT_DIR))
    for name, (hi_res, tile_800, preview) in results:
        print(f"\n{name}")
        print("  hi-res tile :", hi_res)
        print("  800x600 tile:", tile_800)
        print("  preview     :", preview)

    print("\nSuggested CSS:")
    print("""
background-image: url("katakana_tile_1600x1200.png");
background-repeat: repeat;
background-size: 800px 600px;
background-color: white;
""")


if __name__ == "__main__":
    main()
