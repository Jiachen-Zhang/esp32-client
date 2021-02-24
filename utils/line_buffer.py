from typing import List


class LineBuffer:
    LINE_SEPARATOR = '\n'

    def __init__(self) -> None:
        self.buffer = ""

    def assembly_lines(self, msg: str) -> List[str]:
        __buffer = self.buffer + msg
        lines = __buffer.split(self.LINE_SEPARATOR)
        self.buffer = lines[-1]
        return lines[:-1]

    def clear(self):
        self.buffer = ""
