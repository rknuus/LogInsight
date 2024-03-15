from rich.segment import Segment
from textual.strip import Strip
from textual.widget import Widget


class LineView(Widget):
    def __init__(self, file):
        super().__init__()
        self._file = file

    def render_line(self, y: int) -> Strip:
        if y >= self._file.number_of_lines:
            return Strip.blank(self._file.number_of_characters_in_longest_line)

        segments = [Segment(line) for line in self._file.load_lines(y, 1)]
        strip = Strip(segments, self._file.number_of_characters_in_longest_line)
        return strip