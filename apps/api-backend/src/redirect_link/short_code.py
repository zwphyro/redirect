from random import choice


class ShortCodeGenerator:
    def __init__(self, *, length: int = 6):
        self._length = length
        self._symbols = "".join(
            "".join(chr(code) for code in range(ord(start), ord(end) + 1))
            for start, end in [("a", "z"), ("A", "Z"), ("0", "9")]
        )

    def generate(self):
        return "".join(choice(self._symbols) for _ in range(self._length))
