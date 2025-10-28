from LegoPiece import LegoPiece
from LegoColor import LegoColor
from LegoType import LegoType
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from collections import Counter
from Color import Color


def init_parse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Image to Lego Board",
        description="Transform an image into a Lego board plan",
        epilog="Thank you for using this program! - gderybel",
    )

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

    def valid_size(s: str) -> LegoPiece:
        try:
            s = int(s)
        except ValueError:
            raise argparse.ArgumentTypeError(f"size '{s}' is not a valid integer")
        return LegoPiece.get_lego_baseplate_by_size(s)

    parser.add_argument(
        "-s",
        "--size",
        default="32",
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
        closest_color = LegoColor.get_closest_lego_color(Color((r, g, b)))
        mapped.append(LegoPiece(LegoType.PLATE, closest_color, (1, 1)))

    # Turn flat mapped list into matrix rows (height rows, each width long)
    matrix: list[list[LegoPiece]] = [
        mapped[row_start : row_start + w] for row_start in range(0, w * h, w)
    ]
    return matrix


def get_block_list(matrix: list[list[LegoPiece]]) -> None:
    flat = [cell for row in matrix for cell in row]
    counts = Counter()

    for piece in flat:
        # group by reference, color name, and size
        ref = getattr(piece.reference, "name", str(piece.reference))
        col = getattr(
            piece.color, "name", getattr(piece.color, "hex_code", str(piece.color))
        )
        size = piece.size
        key = (ref, col, size)
        counts[key] += 1

    for (ref, col, size), count in counts.most_common():
        plural = "s" if count != 1 else ""
        size_str = f"{size[0]}x{size[1]}"
        print(
            f"You need {count} piece{plural} of type {ref}, color {col}, size {size_str}"
        )


def render_matrix_to_image(
    matrix: list[list[LegoPiece]], stud_size: int = 20, show_studs: bool = True
) -> Image.Image:
    h = len(matrix)
    w = len(matrix[0]) if h else 0

    index_space = stud_size * 2 // 3
    img_w = w * stud_size + index_space
    img_h = h * stud_size + index_space

    img = Image.new("RGB", (img_w, img_h), (240, 240, 240))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    for x in range(w):
        text = str(x + 1)
        tx = index_space + x * stud_size + stud_size // 2
        ty = index_space // 4
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        draw.text(
            (tx - text_w // 2, ty - text_h // 2),
            text,
            fill=(0, 0, 0),
            font=font,
        )

    for y in range(h):
        text = str(y + 1)
        tx = index_space // 4
        ty = index_space + y * stud_size + stud_size // 2
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        draw.text(
            (tx - text_w // 2, ty - text_h // 2),
            text,
            fill=(0, 0, 0),
            font=font,
        )

    for y, row in enumerate(matrix):
        for x, piece in enumerate(row):
            x0 = index_space + x * stud_size
            y0 = index_space + y * stud_size
            x1 = x0 + stud_size
            y1 = y0 + stud_size

            # brick body
            draw.rectangle([x0, y0, x1, y1], fill=piece.color.rgb_code)

            if show_studs:
                # stud: centered circle with slight highlight
                cx = x0 + stud_size / 2
                cy = y0 + stud_size / 2
                r = stud_size * 0.35
                stud_fill = tuple(min(255, int(c * 1.15)) for c in piece.color.rgb_code)
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
    baseplate = args.size

    matrix = image_to_matrix(image_path, baseplate.size)

    get_block_list(matrix)

    out_image = render_matrix_to_image(matrix, stud_size=20, show_studs=True)
    out_path = image_path.parent / f"{image_path.stem}_lego.png"
    out_image.save(out_path)
    print(f"Saved rendered lego image to: {out_path}")


if __name__ == "__main__":
    main()
