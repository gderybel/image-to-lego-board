import LegoColor
import LegoType


class LegoPiece:
    def __init__(self, piece_type: LegoType, color: LegoColor, size: tuple[int, int]):
        self.piece_type = piece_type
        self.color = color
        self.size = size  # e.g., (2, 4) for a 2x4 brick

    # Default baseplate sizes offered by Lego
    BASEPLATE_14_14 = (14, 14) # ref bp02b 
    BASEPLATE_16_16 = (16, 16) # ref 3867
    BASEPLATE_24_24 = (24, 24) # ref 367a
    BASEPLATE_32_32 = (32, 32) # ref 3811
    BASEPLATE_40_40 = (40, 40) # ref bb040
    BASEPLATE_48_48 = (48, 48) # ref 4186
    
