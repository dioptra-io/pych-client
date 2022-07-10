class LineDecoder:
    """
    Faster version of httpx._decoders.LineDecoder.
    It is about 80-100x times faster, depending on line length.
    See https://github.com/encode/httpx/discussions/2300.
    """

    def __init__(self) -> None:
        self.buffer = ""

    def decode(self, text: str) -> list[str]:
        if self.buffer:
            text = self.buffer + text
        lines = text.splitlines()
        if lines and lines[-1] and text and lines[-1][-1] == text[-1]:
            self.buffer = lines.pop()
        else:
            self.buffer = ""
        return lines

    def flush(self) -> list[str]:
        if self.buffer:
            lines = [self.buffer]
        else:
            lines = []
        self.buffer = ""
        return lines
