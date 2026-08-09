from pathlib import Path
from PIL import Image
import shutil
import sys


MAX_WIDTH = 750


def process_image(source: Path, destination: Path) -> None:
    with Image.open(source) as img:
        width, height = img.size

        destination.parent.mkdir(parents=True, exist_ok=True)

        # Do not enlarge images that are already smaller than the limit.
        if width <= MAX_WIDTH:
            shutil.copy2(source, destination)
            print(f"Copied   : {source.name} ({width} x {height})")
            return

        new_height = round(height * MAX_WIDTH / width)

        resized = img.resize(
            (MAX_WIDTH, new_height),
            Image.Resampling.LANCZOS
        )

        resized.save(destination)

        print(
            f"Resized  : {source.name} "
            f"({width} x {height}) -> ({MAX_WIDTH} x {new_height})"
        )


def main():
    if len(sys.argv) != 3:
        print(
            "Usage: python resize_images.py "
            "<source_folder> <output_folder>"
        )
        sys.exit(1)

    source_folder = Path(sys.argv[1])
    output_folder = Path(sys.argv[2])

    extensions = {".png", ".jpg", ".jpeg"}

    for source in source_folder.iterdir():
        if source.is_file() and source.suffix.lower() in extensions:
            destination = output_folder / source.name
            process_image(source, destination)


if __name__ == "__main__":
    main()