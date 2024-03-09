from rich.segment import Segment
from textual.strip import Strip
from textual.widget import Widget


class LineView(Widget):
    def __init__(self, file):
        super().__init__()
        self._file = file

    def render_line(self, y: int) -> Strip:
        if y >= self._file.number_of_lines:
            return Strip.blank(self.size.width)

        segments = [Segment(line) for line in self._file.load_lines(y, 1)]
        # FIXME(KNR): we need the max number of characters, not the number of bytes
        strip = Strip(segments, self._file.number_of_bytes_in_longest_line)
        return strip