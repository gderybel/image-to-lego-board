class Color:
    def __init__(self, hex_code: str):
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
