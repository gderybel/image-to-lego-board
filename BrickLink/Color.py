from functools import lru_cache
from Color import Color as BaseColor
from Brick.Type import Type


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
    @lru_cache(maxsize=None)
    def get_closest_bricklink_color(color: BaseColor) -> "Color":
        from BrickLink.Connector import Connector

        bricklink_colors = Connector.get_piece_colors_with_stock(Type.PLATE)

        # Only get solid and stock > 10 colors
        filtered_colors = [
            color
            for color in bricklink_colors
            if color.type == Color.SOLID and color.stock > 10
        ]

        r1, g1, b1 = color.rgb
        best_dist = float("inf")
        best_color = None
        for bricklink_color in filtered_colors:
            r2, g2, b2 = bricklink_color.rgb_code
            dist = (r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2
            if dist < best_dist:
                best_dist = dist
                best_color = bricklink_color
        if best_color is None:
            raise RuntimeError("No Color constants found / supported formats.")
        return best_color

    @staticmethod
    @lru_cache(maxsize=256)
    def get_bricklink_color_by_name(name: str) -> "Color":
        from BrickLink.Connector import Connector

        bricklink_colors = Connector.get_piece_colors_with_stock(Type.PLATE)
        for bricklink_color in bricklink_colors:
            if bricklink_color.name == name:
                return bricklink_color
        raise ValueError(f"No Color named '{name}'")
