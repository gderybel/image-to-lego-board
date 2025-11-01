from functools import lru_cache
from Color import Color as BaseColor


class Color:
    def __init__(self, id: str, name: str, hex_code: str):
        self.id = id
        self.name = name
        self.hex_code = hex_code
        self.rgb_code = self._to_rgb(hex_code)

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
    def get_closest_bricklink_color(color: BaseColor) -> "Color":
        from BrickLink.Connector import Connector

        bricklink_colors = Connector.get_piece_colors()
        r1, g1, b1 = color.rgb
        best_dist = float("inf")
        best_color = None
        for bricklink_color in bricklink_colors:
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

        bricklink_colors = Connector.get_piece_colors()
        for bricklink_color in bricklink_colors:
            if bricklink_color.name == name:
                return bricklink_color
        raise ValueError(f"No Color named '{name}'")
