from functools import lru_cache


class LegoColor:
    def __init__(self, hex_code):
        self.hex_code = hex_code

    # Color variables
    AQUA = "BCE5DC"
    BLACK = "212121"
    BLUE = "0057A6"
    BRIGHT_GREEN = "10CB31"
    BRIGHT_LIGHT_BLUE = "BCD1ED"
    BRIGHT_LIGHT_ORANGE = "FFC700"
    BRIGHT_LIGHT_YELLOW = "FFF08C"
    BRIGHT_PINK = "F7BCDA"
    BROWN = "6B3F22"
    CORAL = "FF8172"
    DARK_AZURE = "009FE0"
    DARK_BLUE = "243757"
    DARK_BLUISH_GRAY = "595D60"
    DARK_BROWN = "50372F"
    DARK_GRAY = "6B5A5A"
    DARK_GREEN = "2E5543"
    DARK_NOUGAT = "CE7942"
    DARK_ORANGE = "B35408"
    DARK_PINK = "EF5BB3"
    DARK_PURPLE = "5F2683"
    DARK_RED = "6A0E15"
    DARK_TAN = "B89869"
    DARK_TURQUOISE = "00A29F"
    DARK_YELLOW = "DD982E"
    GREEN = "00923D"
    LAVENDER = "D3BDE3"
    LIGHT_AQUA = "CFEFEA"
    LIGHT_BLUISH_GRAY = "AFB5C7"
    LIGHT_BROWN = "99663E"
    LIGHT_GRAY = "9C9C9C"
    LIGHT_GREEN = "D7EED1"
    LIGHT_NOUGAT = "FECCB0"
    LIGHT_ORANGE = "FFBC36"
    LIGHT_SALMON = "FCC7B7"
    LIGHT_TURQUOISE = "00C5BC"
    LIGHT_YELLOW = "FEE89F"
    LIME = "C4E000"
    MAERSK_BLUE = "7DC1D8"
    MAGENTA = "B72276"
    MEDIUM_AZURE = "6ACEE0"
    MEDIUM_BLUE = "82ADD8"
    MEDIUM_LAVENDER = "C689D9"
    MEDIUM_NOUGAT = "E3A05B"
    MEDIUM_ORANGE = "FFA531"
    MEDIUM_VIOLET = "9391E4"
    NEON_YELLOW = "FFFC00"
    NOUGAT = "FFAF7D"
    OLIVE_GREEN = "ABA953"
    ORANGE = "FF7E14"
    PINK = "F5CDD6"
    PURPLE = "7A238D"
    RED = "B30006"
    REDDISH_BROWN = "82422A"
    REDDISH_ORANGE = "FF5500"
    ROSE_PINK = "F2D3D1"
    RUST = "B24817"
    SAND_BLUE = "8899AB"
    SAND_GREEN = "A2BFA3"
    TAN = "EED9A4"
    VERY_LIGHT_BLUISH_GRAY = "E4E8E8"
    VERY_LIGHT_GRAY = "E8E8E8"
    VERY_LIGHT_ORANGE = "FFDCA4"
    WHITE = "FFFFFF"
    YELLOW = "FFE001"
    YELLOWISH_GREEN = "E7F2A7"
    TRANS_AQUA = "B7C8BF"
    TRANS_BLACK = "777777"
    TRANS_BRIGHT_GREEN = "10CB31"
    TRANS_BROWN = "939484"
    TRANS_CLEAR = "EEEEEE"
    TRANS_DARK_BLUE = "00296B"
    TRANS_GREEN = "217625"
    TRANS_LIGHT_BLUE = "68BCC5"
    TRANS_LIGHT_BRIGHT_GREEN = "71EB54"
    TRANS_LIGHT_ORANGE = "E99A3A"
    TRANS_MEDIUM_BLUE = "76A3C8"
    TRANS_NEON_GREEN = "C0F500"
    TRANS_NEON_ORANGE = "FF4231"
    TRANS_NEON_YELLOW = "FFD700"
    TRANS_ORANGE = "E96F01"
    TRANS_PURPLE = "5525B7"
    TRANS_RED = "9C0010"
    TRANS_YELLOW = "EBF72D"
    CHROME_GOLD = "F1F2E1"
    FLAT_DARK_GOLD = "AD7118"
    FLAT_SILVER = "8D949C"
    PEARL_GOLD = "E79E1D"
    PEARL_LIGHT_GOLD = "E7AE5A"
    PEARL_LIGHT_GRAY = "ACB7C0"
    SATIN_TRANS_LIGHT_BLUE = "68BCC5"
    METALLIC_GOLD = "B8860B"
    METALLIC_SILVER = "C0C0C0"
    MILKY_WHITE = "D4D3DD"
    GLITTER_TRANS_LIGHT_BLUE = "68BCC5"

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
    @lru_cache(maxsize=1)
    def get_lego_colors() -> dict[str, tuple[int, int, int]]:
        colors: dict[str, tuple[int, int, int]] = {}
        for name in dir(LegoColor):
            if not name.isupper():
                continue
            try:
                val = getattr(LegoColor, name)
                rgb = LegoColor._to_rgb(val)
                colors[name] = rgb
            except Exception:
                continue
        if not colors:
            raise RuntimeError("No LegoColor constants found / supported formats.")
        return colors

    def get_closest_color(self) -> str:
        r1, g1, b1 = self._to_rgb(self.hex_code)
        best_dist = float("inf")
        best_color = None
        for _, (r2, g2, b2) in self.get_lego_colors().items():
            dist = (r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2
            if dist < best_dist:
                best_dist = dist
                best_color = (r2, g2, b2)
        if best_color is None:
            raise RuntimeError("No LegoColor constants found / supported formats.")
        return best_color
