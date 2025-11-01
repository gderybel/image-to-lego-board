from functools import lru_cache
from BrickLink.Color import Color
from Brick.Type import Type
from urllib.parse import urlencode, urlparse, urlunparse


class Piece:

    baseUrl = "https://www.bricklink.com/v2/catalog/catalogitem.page"

    def __init__(self, reference: Type, color: Color, size: tuple[int, int]):
        self.reference = reference
        self.color = color
        self.size = size  # e.g., (2, 4) for a 2x4 brick

    @staticmethod
    @lru_cache(maxsize=256)
    def get_baseplate_by_size(size: int) -> "Piece":
        size = (size, size)
        for lego_baseplate in lego_baseplates:
            if lego_baseplate.size == size:
                return lego_baseplate
        raise ValueError(
            f"No baseplate with size {size}. Supported sizes: {[bp.size for bp in lego_baseplates]}"
        )

    def get_bricklink_url(self):
        baseUrl = urlparse(self.baseUrl)
        query_parameters = urlencode(
            {"P": self.reference, "C": self.color.bricklink_id}
        )
        fragment = f"T=S&C={self.color.bricklink_id}"
        return urlunparse(baseUrl._replace(query=query_parameters, fragment=fragment))


lego_baseplates = [
    Piece(Type.BASEPLATE_14_14, Color.get_bricklink_color_by_name("White"), (14, 14)),
    Piece(Type.BASEPLATE_16_16, Color.get_bricklink_color_by_name("White"), (16, 16)),
    Piece(Type.BASEPLATE_24_24, Color.get_bricklink_color_by_name("White"), (24, 24)),
    Piece(Type.BASEPLATE_32_32, Color.get_bricklink_color_by_name("White"), (32, 32)),
    Piece(Type.BASEPLATE_40_40, Color.get_bricklink_color_by_name("White"), (40, 40)),
    Piece(Type.BASEPLATE_48_48, Color.get_bricklink_color_by_name("White"), (48, 48)),
]
