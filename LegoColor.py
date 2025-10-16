from functools import lru_cache
from Color import Color


class LegoColor(Color):
    def __init__(self, name: str, hex_code: str):
        self.name = name
        super().__init__(hex_code)

    @staticmethod
    def get_closest_lego_color(color: Color) -> "LegoColor":
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
        key = name.strip().upper()
        for lego_color in lego_colors:
            if lego_color.name == key:
                return lego_color
        raise ValueError(f"No LegoColor named '{name}'")


lego_colors = [
    LegoColor("AQUA", "#BCE5DC"),
    LegoColor("BLACK", "#212121"),
    LegoColor("BLUE", "#0057A6"),
    LegoColor("BRIGHT_GREEN", "#10CB31"),
    LegoColor("BRIGHT_LIGHT_BLUE", "#BCD1ED"),
    LegoColor("BRIGHT_LIGHT_ORANGE", "#FFC700"),
    LegoColor("BRIGHT_LIGHT_YELLOW", "#FFF08C"),
    LegoColor("BRIGHT_PINK", "#F7BCDA"),
    LegoColor("BROWN", "#6B3F22"),
    LegoColor("CORAL", "#FF8172"),
    LegoColor("DARK_AZURE", "#009FE0"),
    LegoColor("DARK_BLUE", "#243757"),
    LegoColor("DARK_BLUISH_GRAY", "#595D60"),
    LegoColor("DARK_BROWN", "#50372F"),
    LegoColor("DARK_GRAY", "#6B5A5A"),
    LegoColor("DARK_GREEN", "#2E5543"),
    LegoColor("DARK_NOUGAT", "#CE7942"),
    LegoColor("DARK_ORANGE", "#B35408"),
    LegoColor("DARK_PINK", "#EF5BB3"),
    LegoColor("DARK_PURPLE", "#5F2683"),
    LegoColor("DARK_RED", "#6A0E15"),
    LegoColor("DARK_TAN", "#B89869"),
    LegoColor("DARK_TURQUOISE", "#00A29F"),
    LegoColor("DARK_YELLOW", "#DD982E"),
    LegoColor("GREEN", "#00923D"),
    LegoColor("LAVENDER", "#D3BDE3"),
    LegoColor("LIGHT_AQUA", "#CFEFEA"),
    LegoColor("LIGHT_BLUISH_GRAY", "#AFB5C7"),
    LegoColor("LIGHT_BROWN", "#99663E"),
    LegoColor("LIGHT_GRAY", "#9C9C9C"),
    LegoColor("LIGHT_GREEN", "#D7EED1"),
    LegoColor("LIGHT_NOUGAT", "#FECCB0"),
    LegoColor("LIGHT_ORANGE", "#FFBC36"),
    LegoColor("LIGHT_SALMON", "#FCC7B7"),
    LegoColor("LIGHT_TURQUOISE", "#00C5BC"),
    LegoColor("LIGHT_YELLOW", "#FEE89F"),
    LegoColor("LIME", "#C4E000"),
    LegoColor("MAERSK_BLUE", "#7DC1D8"),
    LegoColor("MAGENTA", "#B72276"),
    LegoColor("MEDIUM_AZURE", "#6ACEE0"),
    LegoColor("MEDIUM_BLUE", "#82ADD8"),
    LegoColor("MEDIUM_LAVENDER", "#C689D9"),
    LegoColor("MEDIUM_NOUGAT", "#E3A05B"),
    LegoColor("MEDIUM_ORANGE", "#FFA531"),
    LegoColor("MEDIUM_VIOLET", "#9391E4"),
    LegoColor("NEON_YELLOW", "#FFFC00"),
    LegoColor("NOUGAT", "#FFAF7D"),
    LegoColor("OLIVE_GREEN", "#ABA953"),
    LegoColor("ORANGE", "#FF7E14"),
    LegoColor("PINK", "#F5CDD6"),
    LegoColor("PURPLE", "#7A238D"),
    LegoColor("RED", "#B30006"),
    LegoColor("REDDISH_BROWN", "#82422A"),
    LegoColor("REDDISH_ORANGE", "#FF5500"),
    LegoColor("ROSE_PINK", "#F2D3D1"),
    LegoColor("RUST", "#B24817"),
    LegoColor("SAND_BLUE", "#8899AB"),
    LegoColor("SAND_GREEN", "#A2BFA3"),
    LegoColor("TAN", "#EED9A4"),
    LegoColor("VERY_LIGHT_BLUISH_GRAY", "#E4E8E8"),
    LegoColor("VERY_LIGHT_GRAY", "#E8E8E8"),
    LegoColor("VERY_LIGHT_ORANGE", "#FFDCA4"),
    LegoColor("WHITE", "#FFFFFF"),
    LegoColor("YELLOW", "#FFE001"),
    LegoColor("YELLOWISH_GREEN", "#E7F2A7"),
    LegoColor("TRANS_AQUA", "#B7C8BF"),
    LegoColor("TRANS_BLACK", "#777777"),
    LegoColor("TRANS_BRIGHT_GREEN", "#10CB31"),
    LegoColor("TRANS_BROWN", "#939484"),
    LegoColor("TRANS_CLEAR", "#EEEEEE"),
    LegoColor("TRANS_DARK_BLUE", "#00296B"),
    LegoColor("TRANS_GREEN", "#217625"),
    LegoColor("TRANS_LIGHT_BLUE", "#68BCC5"),
    LegoColor("TRANS_LIGHT_BRIGHT_GREEN", "#71EB54"),
    LegoColor("TRANS_LIGHT_ORANGE", "#E99A3A"),
    LegoColor("TRANS_MEDIUM_BLUE", "#76A3C8"),
    LegoColor("TRANS_NEON_GREEN", "#C0F500"),
    LegoColor("TRANS_NEON_ORANGE", "#FF4231"),
    LegoColor("TRANS_NEON_YELLOW", "#FFD700"),
    LegoColor("TRANS_ORANGE", "#E96F01"),
    LegoColor("TRANS_PURPLE", "#5525B7"),
    LegoColor("TRANS_RED", "#9C0010"),
    LegoColor("TRANS_YELLOW", "#EBF72D"),
    LegoColor("CHROME_GOLD", "#F1F2E1"),
    LegoColor("FLAT_DARK_GOLD", "#AD7118"),
    LegoColor("FLAT_SILVER", "#8D949C"),
    LegoColor("PEARL_GOLD", "#E79E1D"),
    LegoColor("PEARL_LIGHT_GOLD", "#E7AE5A"),
    LegoColor("PEARL_LIGHT_GRAY", "#ACB7C0"),
    LegoColor("SATIN_TRANS_LIGHT_BLUE", "#68BCC5"),
    LegoColor("METALLIC_GOLD", "#B8860B"),
    LegoColor("METALLIC_SILVER", "#C0C0C0"),
    LegoColor("MILKY_WHITE", "#D4D3DD"),
    LegoColor("GLITTER_TRANS_LIGHT_BLUE", "#68BCC5"),
]
