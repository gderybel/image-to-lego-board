from functools import lru_cache
from LegoColor import LegoColor
from LegoType import LegoType


class LegoPiece:
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


lego_baseplates = [
    LegoPiece(
        LegoType.BASEPLATE_14_14, LegoColor.get_lego_color_by_name("WHITE"), (14, 14)
    ),
    LegoPiece(
        LegoType.BASEPLATE_16_16, LegoColor.get_lego_color_by_name("WHITE"), (16, 16)
    ),
    LegoPiece(
        LegoType.BASEPLATE_24_24, LegoColor.get_lego_color_by_name("WHITE"), (24, 24)
    ),
    LegoPiece(
        LegoType.BASEPLATE_32_32, LegoColor.get_lego_color_by_name("WHITE"), (32, 32)
    ),
    LegoPiece(
        LegoType.BASEPLATE_40_40, LegoColor.get_lego_color_by_name("WHITE"), (40, 40)
    ),
    LegoPiece(
        LegoType.BASEPLATE_48_48, LegoColor.get_lego_color_by_name("WHITE"), (48, 48)
    ),
]
