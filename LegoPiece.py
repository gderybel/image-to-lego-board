from functools import lru_cache
from LegoColor import LegoColor
from LegoType import LegoType
from urllib.parse import urlencode, urlparse, urlunparse


class LegoPiece:

    baseUrl = "https://www.bricklink.com/v2/catalog/catalogitem.page"

    def __init__(self, reference: LegoType, color: LegoColor, size: tuple[int, int]):
        self.reference = reference
        self.color = color
        self.size = size  # e.g., (2, 4) for a 2x4 brick

    @staticmethod
    @lru_cache(maxsize=256)
    def get_lego_baseplate_by_size(size: int) -> "LegoPiece":
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
    LegoPiece(
        LegoType.BASEPLATE_14_14, LegoColor.get_lego_color_by_name("White"), (14, 14)
    ),
    LegoPiece(
        LegoType.BASEPLATE_16_16, LegoColor.get_lego_color_by_name("White"), (16, 16)
    ),
    LegoPiece(
        LegoType.BASEPLATE_24_24, LegoColor.get_lego_color_by_name("White"), (24, 24)
    ),
    LegoPiece(
        LegoType.BASEPLATE_32_32, LegoColor.get_lego_color_by_name("White"), (32, 32)
    ),
    LegoPiece(
        LegoType.BASEPLATE_40_40, LegoColor.get_lego_color_by_name("White"), (40, 40)
    ),
    LegoPiece(
        LegoType.BASEPLATE_48_48, LegoColor.get_lego_color_by_name("White"), (48, 48)
    ),
]
