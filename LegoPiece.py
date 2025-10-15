import LegoColor
import LegoType


class LegoPiece:
    def __init__(self, type: LegoType, color: LegoColor, size):
        self.type = type
        self.color = color
        self.size = size  # e.g., (2, 4) for a 2x4 brick
