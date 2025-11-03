from functools import lru_cache
from BrickLink.Color import Color
from BrickLink.Item import Item
from Brick.Type import Type
from urllib.parse import urlencode, urlparse, urlunparse


class Piece:

    baseUrl = "https://www.bricklink.com/v2/catalog/catalogitem.page"

    def __init__(self, reference: Type, color: Color, size: tuple[int, int], id: Item):
        self.reference = reference
        self.color = color
        self.size = size  # e.g., (2, 4) for a 2x4 brick
        self.id = id

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
    Piece(
        Type.BASEPLATE_14_14,
        Color.get_bricklink_color_by_name("Green", Type.BASEPLATE_14_14),
        (14, 14),
        Item.BASEPLATE_14_14,
    ),
    Piece(
        Type.BASEPLATE_16_16,
        Color.get_bricklink_color_by_name("White", Type.BASEPLATE_16_16),
        (16, 16),
        Item.BASEPLATE_16_16,
    ),
    Piece(
        Type.BASEPLATE_24_24,
        Color.get_bricklink_color_by_name("Light Gray", Type.BASEPLATE_24_24),
        (24, 24),
        Item.BASEPLATE_24_24,
    ),
    Piece(
        Type.BASEPLATE_32_32,
        Color.get_bricklink_color_by_name("White", Type.BASEPLATE_32_32),
        (32, 32),
        Item.BASEPLATE_32_32,
    ),
    Piece(
        Type.BASEPLATE_40_40,
        Color.get_bricklink_color_by_name("Green", Type.BASEPLATE_40_40),
        (40, 40),
        Item.BASEPLATE_40_40,
    ),
    Piece(
        Type.BASEPLATE_48_48,
        Color.get_bricklink_color_by_name("White", Type.BASEPLATE_48_48),
        (48, 48),
        Item.BASEPLATE_48_48,
    ),
]
