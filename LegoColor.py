from functools import lru_cache
from Color import Color


class LegoColor(Color):
    def __init__(
        self,
        bricklink_name: str,
        lego_name: str,
        bricklink_id: str,
        lego_id: str,
        hex_code: str,
    ):
        self.bricklink_name = bricklink_name
        self.lego_name = lego_name
        self.bricklink_id = bricklink_id
        self.lego_id = lego_id
        super().__init__(hex_code)

    @staticmethod
    def get_closest_lego_color(color: Color) -> "LegoColor":
        from BrickLinkConnector import BrickLinkConnector

        lego_colors = BrickLinkConnector.get_piece_colors()
        r1, g1, b1 = color.rgb_code
        best_dist = float("inf")
        best_color = None
        for lego_color in lego_colors:
            r2, g2, b2 = lego_color.rgb_code
            dist = (r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2
            if dist < best_dist:
                best_dist = dist
                best_color = lego_color
        if best_color is None:
            raise RuntimeError("No LegoColor constants found / supported formats.")
        return best_color

    @staticmethod
    @lru_cache(maxsize=256)
    def get_lego_color_by_name(name: str) -> "LegoColor":
        from BrickLinkConnector import BrickLinkConnector

        lego_colors = BrickLinkConnector.get_piece_colors()
        for lego_color in lego_colors:
            if lego_color.lego_name == name:
                return lego_color
        raise ValueError(f"No LegoColor named '{name}'")
