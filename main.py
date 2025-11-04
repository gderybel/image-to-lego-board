from Brick.Piece import Piece
from Brick.Type import Type
from BrickLink.Item import Item
from BrickLink.Color import Color as BrickLinkColor
import argparse
from pathlib import Path
from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont
from collections import Counter
from Color import Color
from BrickLink.Connector import Connector
from datetime import datetime
from skimage import io, color


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

    def valid_size(s: str) -> Piece:
        try:
            s = int(s)
        except ValueError:
            raise argparse.ArgumentTypeError(f"size '{s}' is not a valid integer")
        return Piece.get_baseplate_by_size(s)

    parser.add_argument(
        "-s",
        "--size",
        default="32",
        type=valid_size,
        help="Size of the Lego baseplate (default: 32)",
    )

    parser.add_argument(
        "-j",
        "--jwt",
        help='JWT Token for BrickLink auth, value is from Cookie named "bricklink.bricklink-account.jwt". If given, will create a wishlist.',
        default=None,
    )

    available_types = {
        "plate": Type.PLATE,
        "plate_round": Type.PLATE_ROUND,
        "slope": Type.SLOPE,
        "tile": Type.TILE,
    }

    def valid_type(s: str) -> Type:
        if s not in available_types:
            valid_values = ", ".join(available_types.keys())
            raise argparse.ArgumentTypeError(
                f"Type '{s}' is not a valid type. Must be one of: {valid_values}"
            )
        return available_types[s]

    parser.add_argument(
        "-t",
        "--type",
        help=(
            "Types available are:\n"
            + ",".join(f" {key} ({value})" for key, value in available_types.items())
        ),
        default="plate",
        type=valid_type,
    )

    return parser


def print_color(text: str, color: tuple[int, int, int]):
    r, g, b = color
    print(f"\033[48;2;{r};{g};{b}m  {text}  \033[0m")


def image_to_matrix(
    image_path: Path, size: tuple[int, int], piece_type: Type
) -> list[list[str]]:
    w, h = size
    img = Image.open(image_path).convert("RGB").resize((w, h), Image.LANCZOS)
    resized_path = image_path.parent / f"{image_path.stem}_resized_{w}x{h}.png"
    img.save(resized_path)

    rgb = io.imread(resized_path)
    pixels = color.rgb2lab(rgb)
    flat_pixels = pixels.reshape(-1, 3)

    # transform colors for each pixel to nearest Lego color
    mapped = []
    for l, a, b in tqdm(flat_pixels, desc="Mapping colors", unit="pixel"):
        closest_color = BrickLinkColor.get_closest_bricklink_color(
            Color(l, a, b), piece_type
        )
        mapped.append(Piece(piece_type, closest_color, (1, 1), Item.PLATE))

    # Turn flat mapped list into matrix rows (height rows, each width long)
    matrix: list[list[Piece]] = [
        mapped[row_start : row_start + w] for row_start in range(0, w * h, w)
    ]
    return matrix


def get_block_list(matrix: list[list[Piece]], jwt: str = None) -> None:
    flat = [cell for row in matrix for cell in row]
    counts = Counter()
    piece_map = {}

    if jwt:
        wishlist = Connector.create_wishlist(f"Project {datetime.now()}", jwt=jwt)
        # Add baseplate
        Connector.add_piece_to_wishlist(
            wishlist, Piece.get_baseplate_by_size(len(matrix)), 1, jwt
        )

    for piece in flat:
        ref = getattr(piece.reference, "name", str(piece.reference))
        col = getattr(piece.color, "id", str(piece.color))
        col_rgb = getattr(piece.color, "rgb_code", (255, 255, 255))
        size = piece.size
        key = (ref, col, size, col_rgb)

        counts[key] += 1
        piece_map[key] = piece

    for (ref, col, size, col_rgb), count in counts.most_common():
        plural = "s" if count != 1 else ""
        size_str = f"{size[0]}x{size[1]}"
        stock, url = Connector.get_piece_stock(ref=ref, color_id=col, quantity=count)

        if jwt:
            piece = piece_map[(ref, col, size, col_rgb)]
            Connector.add_piece_to_wishlist(wishlist, piece, count, jwt)

        print_color(
            f"You need {count} piece{plural} from {url} (ref: {ref}, color: {col}, size: {size_str}, stock: {stock})",
            col_rgb,
        )

    if jwt:
        url = Connector.get_wishlist_url(wishlist)
        print(f"Wishlist `{wishlist.name}` created: {url}.")


def render_matrix_to_image(
    matrix: list[list[Piece]], stud_size: int = 20, show_studs: bool = True
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
    jwt = args.jwt
    piece_type = args.type

    matrix = image_to_matrix(image_path, baseplate.size, piece_type)

    print("Building baseplate...")
    get_block_list(matrix, jwt)
    print("Baseplate fully prepared.")

    print("Rendering matrix to image...")
    out_image = render_matrix_to_image(matrix, stud_size=20, show_studs=True)
    out_path = image_path.parent / f"{image_path.stem}_brick.png"
    out_image.save(out_path)
    print(f"Saved rendered Lego image to: {out_path}")


if __name__ == "__main__":
    main()
