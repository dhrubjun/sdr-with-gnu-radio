from pathlib import Path
from PIL import Image, ImageDraw

# ============================================================
# USER CONFIGURATION
# ============================================================

INPUT_DIR = Path("figures/ch08/originals")
OUTPUT_FILE = Path("figures/ch08/ch08-exp2-real-downconversion-comparison.png")

FILES = [
    ("lo-4khz.png", "(a) LO = 4 kHz"),
    ("lo-5khz.png", "(b) LO = 5 kHz"),
    ("lo-5-5khz.png", "(c) LO = 5.5 kHz"),
    ("lo-6khz.png", "(d) LO = 6 kHz"),
    ("lo-6-5khz.png", "(e) LO = 6.5 kHz"),
]

# Number of columns in the montage.
COLUMNS = 2

# Display width of each screenshot.
PANEL_WIDTH = 700

# Space reserved above each panel for its label.
LABEL_HEIGHT = 42

# Horizontal and vertical gaps between panels.
GAP_X = 20
GAP_Y = 20

BACKGROUND = "white"

# ============================================================
# PANEL PREPARATION
# ============================================================

def prepare_panel(filename, label):
    path = INPUT_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Missing input image: {path}")

    img = Image.open(path).convert("RGB")

    # Resize while preserving aspect ratio.
    ratio = PANEL_WIDTH / img.width
    new_height = round(img.height * ratio)

    img = img.resize(
        (PANEL_WIDTH, new_height),
        Image.Resampling.LANCZOS
    )

    # Create panel with space above for the label.
    panel = Image.new(
        "RGB",
        (PANEL_WIDTH, new_height + LABEL_HEIGHT),
        BACKGROUND
    )

    panel.paste(img, (0, LABEL_HEIGHT))

    draw = ImageDraw.Draw(panel)

    draw.text(
        (12, 10),
        label,
        fill="black"
    )

    return panel


# ============================================================
# CREATE PANELS
# ============================================================

panels = [
    prepare_panel(filename, label)
    for filename, label in FILES
]

# Normalize panel heights.
max_panel_height = max(panel.height for panel in panels)

normalized_panels = []

for panel in panels:
    canvas = Image.new(
        "RGB",
        (PANEL_WIDTH, max_panel_height),
        BACKGROUND
    )

    canvas.paste(panel, (0, 0))
    normalized_panels.append(canvas)


# ============================================================
# LAYOUT
# ============================================================

rows = (len(normalized_panels) + COLUMNS - 1) // COLUMNS

final_width = (
    COLUMNS * PANEL_WIDTH
    + (COLUMNS - 1) * GAP_X
)

final_height = (
    rows * max_panel_height
    + (rows - 1) * GAP_Y
)

combined = Image.new(
    "RGB",
    (final_width, final_height),
    BACKGROUND
)


# ============================================================
# PLACE PANELS
# ============================================================

for index, panel in enumerate(normalized_panels):
    row = index // COLUMNS
    col = index % COLUMNS

    x = col * (PANEL_WIDTH + GAP_X)
    y = row * (max_panel_height + GAP_Y)

    # If the final row is incomplete, center its panels.
    items_in_last_row = len(normalized_panels) % COLUMNS

    if (
        row == rows - 1
        and items_in_last_row != 0
        and items_in_last_row < COLUMNS
    ):
        used_width = (
            items_in_last_row * PANEL_WIDTH
            + (items_in_last_row - 1) * GAP_X
        )

        start_x = (final_width - used_width) // 2

        position_in_last_row = index - (rows - 1) * COLUMNS

        x = (
            start_x
            + position_in_last_row * (PANEL_WIDTH + GAP_X)
        )

    combined.paste(panel, (x, y))


# ============================================================
# SAVE
# ============================================================

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

combined.save(
    OUTPUT_FILE,
    quality=95
)

print(f"Saved: {OUTPUT_FILE}")
print(f"Final size: {combined.width} x {combined.height}")