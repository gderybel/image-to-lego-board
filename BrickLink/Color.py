from Color import Color as BaseColor, CIEDE2000
from functools import lru_cache
from Brick.Type import Type
from skimage import color


class Color:
    # types
    SOLID = "solid"
    PEARL = "pearl"
    METALLIC = "metallic"
    TRANS = "trans"
    GLITTER = "glitter"
    CHROME = "chrome"

    def __init__(self, id: str, name: str, hex_code: str, stock: int):
        self.id = id
        self.name = name
        self.hex_code = hex_code
        self.stock = stock
        self.rgb_code = self._to_rgb(hex_code)
        self.lab_code = self._to_lab(hex_code)

        self.type = self.SOLID
        if Color.PEARL in self.name.lower():
            self.type = Color.PEARL
        elif Color.METALLIC in self.name.lower():
            self.type = Color.METALLIC
        elif Color.TRANS in self.name.lower():
            self.type = Color.TRANS
        elif Color.GLITTER in self.name.lower():
            self.type = Color.GLITTER
        elif Color.CHROME in self.name.lower():
            self.type = Color.CHROME

    @staticmethod
    def _to_rgb(v) -> tuple[int, int, int]:
        if isinstance(v, (tuple, list)) and len(v) == 3:
            return (int(v[0]), int(v[1]), int(v[2]))
        if isinstance(v, str):
            s = v.lstrip("#")
            if len(s) == 6:
                return tuple(int(s[i : i + 2], 16) for i in (0, 2, 4))
        raise ValueError(f"unsupported color format: {v!r}")

    @staticmethod
    def _to_lab(v) -> tuple[int, int, int]:
        rgb = Color._to_rgb(v)
        rgb_normalized = [c / 255 for c in rgb]
        return color.rgb2lab(rgb_normalized)

    @staticmethod
    @lru_cache(maxsize=None)
    def get_closest_bricklink_color(color: BaseColor, piece_type: Type) -> "Color":
        from BrickLink.Connector import Connector

        bricklink_colors = Connector.get_piece_colors_with_stock(piece_type)

        # Only get solid and stock > 10 colors
        filtered_colors = [
            color
            for color in bricklink_colors
            if color.type == Color.SOLID and color.stock > 10
        ]
        best_dist = float("inf")
        best_color = None
        for bricklink_color in filtered_colors:
            dist = CIEDE2000(color.lab, bricklink_color.lab_code)
            if dist < best_dist:
                best_dist = dist
                best_color = bricklink_color
        if best_color is None:
            raise RuntimeError("No Color constants found / supported formats.")
        return best_color

    @staticmethod
    @lru_cache(maxsize=256)
    def get_bricklink_color_by_name(name: str, piece_type: Type) -> "Color":
        from BrickLink.Connector import Connector

        bricklink_colors = Connector.get_piece_colors_with_stock(piece_type)
        for bricklink_color in bricklink_colors:
            if bricklink_color.name == name:
                return bricklink_color
        raise ValueError(f"No Color named '{name}'")
