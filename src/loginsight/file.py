from pathlib import Path
import mmap
import os

class File:
    '''
    File represents a file to be analyzed.

    The class is designed to analyze large files with reasonable reaction times when using a
    textual based TUI (see textualize.io). As the TUI only displays a fixed set of lines at a time
    the method load_lines(starting_at_line_number, number_of_lines) supports loading of lines.
    '''

    def __init__(self, file_path: Path):
        self._path = file_path

        # We use binary mode, because we build up lists of newline positions and line lengths
        # (both in bytes) and use those lists to navigate the file ourselves instead of using
        # readlines(). For the same reason we also disable buffering.
        self._file = open(self._path, 'rb', buffering=0)
        self._file.seek(0, os.SEEK_END)
        self._size = self._file.tell()

        # TODO(KNR): check if the scan is best done in the background
        self._line_start_positions, self._number_of_bytes_in_line = self._scan_line_positions()
        # TODO(KNR): benchmark assigning max to the member variable in every loop
        self._number_of_bytes_in_longest_line = max(self._number_of_bytes_in_line) if self._number_of_bytes_in_line else 0

    @property
    def path(self) -> Path:
        return self._path

    @property
    def size_in_bytes(self) -> int:
        return self._size

    @property
    def number_of_lines(self) -> int:
        return len(self._line_start_positions)

    @property
    def number_of_bytes_in_longest_line(self) -> int:
        return self._number_of_bytes_in_longest_line

    def load_lines(self, starting_at_line_number, number_of_lines) -> list[str]:
        if starting_at_line_number < 0:
            # TODO(KNR): use structured logging to capture context
            raise ValueError('starting_at_line_number is {} but must be at least 0'.format(starting_at_line_number))
        if number_of_lines < 1:
            raise ValueError('number_of_lines is {} but must be at least 1'.format(number_of_lines))

        available_number_of_lines = len(self._number_of_bytes_in_line)
        if starting_at_line_number + number_of_lines > available_number_of_lines:
            raise EOFError

        # TODO(KNR): any caching?
        number_of_newlines = (number_of_lines - 1)
        last_line = starting_at_line_number + number_of_lines
        requested_number_of_bytes = sum(self._number_of_bytes_in_line[starting_at_line_number:last_line]) + number_of_newlines
        start_at_byte = self._line_start_positions[starting_at_line_number]
        # TODO(KNR): explore whether os.preadv() would help to keep the memory consumption in check
        # even though textual.Strip objects are immutable
        raw_bytes = os.pread(self._fileno,
                             requested_number_of_bytes,
                             start_at_byte)
        lines = (raw_bytes.decode('utf-8', errors='replace')
                         .expandtabs(4)
                         .split('\n'))
        return lines[0:number_of_lines]

    @property
    def _fileno(self) -> int:
        assert self._file is not None
        return self._file.fileno()

    def _scan_line_positions(self) -> tuple[list[int], list[int]]:
        '''
        Scans for newlines and returns two lists, one with all the line start positions and one with
        all the line lengths. Those information are used by method load_lines().

        Note that the last line might start past EOF if the last character is a newline. But in this
        case the line length is 0, so it does not impact the number of total bytes of multiple lines.
        '''

        if self.size_in_bytes == 0:
            return [], []

        with mmap.mmap(self._fileno, self.size_in_bytes, prot=mmap.PROT_READ) as memory_mapped_file:
            # both in unit bytes
            line_start_positions: list[int] = []
            line_lengths: list[int] = []

            # TODO(KNR): optimize similar to toolong/src/toolong/log_file.py to yield batches to
            # improve reactivity
            previous_newline_position = -1
            while (newline_position := memory_mapped_file.find(b'\n', previous_newline_position + 1)) != -1:
                start_at = previous_newline_position + 1  # +1 to skip newline character
                end_at = newline_position
                previous_newline_position = newline_position

                length = end_at - start_at
                line_start_positions.append(start_at)
                line_lengths.append(length)

            start_at = previous_newline_position + 1  # +1 to skip newline character
            end_at = self.size_in_bytes

            length = end_at - start_at
            line_start_positions.append(start_at)
            line_lengths.append(length)

            return line_start_positions, line_lengths
