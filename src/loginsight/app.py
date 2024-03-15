from loginsight.lineview import LineView
from textual.app import App, ComposeResult


class InteractiveLogViewer(App):
    def __init__(self, file):
        super().__init__()
        self._file = file

    def compose(self) -> ComposeResult:
        yield LineView(self._file)
