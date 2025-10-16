from LegoPiece import LegoPiece
from LegoColor import LegoColor
from LegoType import LegoType
import argparse
from pathlib import Path
from PIL import Image, ImageDraw
from collections import Counter


def init_parse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Image to Lego Board",
        description="Transform an image into a Lego board plan",
        epilog="Thank you for using this program! - gderybel",
    )

    # build a list of available baseplate sizes from LegoPiece constants
    available_sizes = sorted(
        {getattr(LegoPiece, a)[0] for a in dir(LegoPiece) if a.startswith("BASEPLATE_")}
    )
    sizes_str = ", ".join(str(s) for s in available_sizes)

    def valid_image_path(p: str) -> Path:
        path = Path(p)
        if not path.is_file():
            raise argparse.ArgumentTypeError(
                f"image_path '{p}' does not exist or is not a file"
            )
        return path

    parser.add_argument(
        "image_path", help="Path to the input image file", type=valid_image_path
    )

    def valid_size(s: str) -> int:
        try:
            size = int(s)
        except ValueError:
            raise argparse.ArgumentTypeError(f"size '{s}' is not a valid integer")
        attr = f"BASEPLATE_{size}_{size}"
        if not hasattr(LegoPiece, attr):
            raise argparse.ArgumentTypeError(
                f"size '{size}' is not supported. Sizes available are : {sizes_str}."
            )
        return getattr(LegoPiece, attr)

    parser.add_argument(
        "-s",
        "--size",
        default=LegoPiece.BASEPLATE_32_32,
        type=valid_size,
        help="Size of the Lego baseplate (default: 32)",
    )

    return parser


def image_to_matrix(image_path: Path, size: tuple[int, int]) -> list[list[str]]:
    w, h = size
    img = Image.open(image_path).convert("RGB").resize((w, h), Image.LANCZOS)
    # resized_path = image_path.parent / f"{image_path.stem}_resized_{w}x{h}.png"
    # print(f"Saved resized image to: {resized_path}")
    # img.save(resized_path)
    pixels = list(img.getdata())

    # transform colors for each pixel to nearest Lego color
    mapped = []
    for r, g, b in pixels:
        closest_color = LegoColor((r, g, b)).get_closest_color()
        mapped.append(closest_color)

    # Turn flat mapped list into matrix rows (height rows, each width long)
    matrix: list[list[tuple[int, int, int]]] = [
        mapped[row_start : row_start + w] for row_start in range(0, w * h, w)
    ]
    return matrix


def get_block_list(matrix: list[list]) -> None:
    flat = [cell for row in matrix for cell in row]
    counts = Counter(flat)

    for color, count in counts.most_common():
        plural = "s" if count != 1 else ""
        print(f"You need {count} piece{plural} of color {color}")


def render_matrix_to_image(
    matrix: list[list[str]], stud_size: int = 20, show_studs: bool = True
) -> Image.Image:
    h = len(matrix)
    w = len(matrix[0]) if h else 0
    img_w = w * stud_size
    img_h = h * stud_size

    img = Image.new("RGB", (img_w, img_h), (240, 240, 240))
    draw = ImageDraw.Draw(img)

    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            x0 = x * stud_size
            y0 = y * stud_size
            x1 = x0 + stud_size
            y1 = y0 + stud_size

            # brick body
            draw.rectangle([x0, y0, x1, y1], fill=cell)

            if show_studs:
                # stud: centered circle with slight highlight
                cx = x0 + stud_size / 2
                cy = y0 + stud_size / 2
                r = stud_size * 0.35
                stud_fill = tuple(min(255, int(c * 1.15)) for c in cell)
                outline = (0, 0, 0)
                draw.ellipse(
                    [cx - r, cy - r, cx + r, cy + r], fill=stud_fill, outline=outline
                )

    return img


def main():
    # Parse command-line arguments
    parser = init_parse()
    args = parser.parse_args()
    image_path = args.image_path
    size = args.size

    # Define default baseplate
    baseplate = LegoPiece(LegoType.BASEPLATE, LegoColor.WHITE, size)
    matrix = image_to_matrix(image_path, baseplate.size)

    get_block_list(matrix)

    out_image = render_matrix_to_image(matrix, stud_size=20, show_studs=True)
    out_path = image_path.parent / f"{image_path.stem}_lego.png"
    out_image.save(out_path)
    print(f"Saved rendered lego image to: {out_path}")


main()
