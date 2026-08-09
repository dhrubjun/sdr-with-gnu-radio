from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont


INPUT_DIR = Path("figures/ch03/originals")
OUTPUT_FILE = Path("figures/ch03/sampling-rate-comparison.png")

FILES = [
    ("sampling-32ksps.png", "(a) 32 kS/s"),
    ("sampling-8ksps.png", "(b) 8 kS/s"),
    ("sampling-4ksps.png", "(c) 4 kS/s"),
    ("sampling-2-5ksps.png", "(d) 2.5 kS/s"),
]

PANEL_WIDTH = 360
LABEL_HEIGHT = 35
GAP = 12


def prepare_panel(filename, label):
    img = Image.open(INPUT_DIR / filename).convert("RGB")

    # Resize while preserving aspect ratio.
    ratio = PANEL_WIDTH / img.width
    new_height = round(img.height * ratio)

    img = img.resize(
        (PANEL_WIDTH, new_height),
        Image.Resampling.LANCZOS
    )

    # Add space above for the panel label.
    panel = Image.new(
        "RGB",
        (PANEL_WIDTH, new_height + LABEL_HEIGHT),
        "white"
    )

    panel.paste(img, (0, LABEL_HEIGHT))

    draw = ImageDraw.Draw(panel)
    draw.text(
        (10, 8),
        label,
        fill="black"
    )

    return panel


panels = [prepare_panel(name, label) for name, label in FILES]

# Make all panels the same height.
max_height = max(panel.height for panel in panels)

normalized = []
for panel in panels:
    canvas = Image.new(
        "RGB",
        (PANEL_WIDTH, max_height),
        "white"
    )
    canvas.paste(panel, (0, 0))
    normalized.append(canvas)

final_width = PANEL_WIDTH * 2 + GAP
final_height = max_height * 2 + GAP

combined = Image.new(
    "RGB",
    (final_width, final_height),
    "white"
)

combined.paste(normalized[0], (0, 0))
combined.paste(normalized[1], (PANEL_WIDTH + GAP, 0))
combined.paste(normalized[2], (0, max_height + GAP))
combined.paste(
    normalized[3],
    (PANEL_WIDTH + GAP, max_height + GAP)
)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
combined.save(OUTPUT_FILE)

print(f"Saved: {OUTPUT_FILE}")
print(f"Final size: {combined.width} x {combined.height}")