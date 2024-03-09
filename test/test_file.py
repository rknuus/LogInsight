import pytest
from loginsight.file import File


@pytest.fixture
def generate_file_on_disk(tmp_path):
    def _generate_file_factory_function(content):
        file_path = tmp_path / 'file'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return file_path
    return _generate_file_factory_function


# FIXME(KNR): cover non-existing file, existing file without necessary permissions etc.

def test_invalid_parameters_of_lines(generate_file_on_disk):
    file_path = generate_file_on_disk(content='foobar')
    file = File(file_path)

    with pytest.raises(ValueError):
        file.load_lines(-1, 1)
    with pytest.raises(ValueError):
        file.load_lines(1, 0)


def test_empty_file(generate_file_on_disk):
    file_path = generate_file_on_disk(content='')
    file = File(file_path)

    assert file.size_in_bytes == 0
    assert file.number_of_lines == 0
    assert file.number_of_bytes_in_longest_line == 0
    assert file.number_of_characters_in_longest_line == 0

    with pytest.raises(EOFError):
        file.load_lines(0, 1)


def test_file_with_non_newline_characters(generate_file_on_disk):
    file_path = generate_file_on_disk(content='foo')
    file = File(file_path)

    assert file.size_in_bytes == 3
    assert file.number_of_lines == 1
    assert file.number_of_bytes_in_longest_line == 3
    assert file.number_of_characters_in_longest_line == 3

    lines = file.load_lines(0, 1)
    assert len(lines) == 1
    assert lines[0] == 'foo'

    with pytest.raises(EOFError):
        file.load_lines(0, 2)

def test_file_with_single_newline_character(generate_file_on_disk):
    file_path = generate_file_on_disk(content='\n')
    file = File(file_path)

    assert(file.number_of_lines == 2)
    assert file.number_of_bytes_in_longest_line == 0
    assert file.number_of_characters_in_longest_line == 0

    lines = file.load_lines(0, 1)
    assert len(lines) == 1
    assert lines[0] == ''

    lines = file.load_lines(0, 2)
    assert len(lines) == 2
    assert lines[0] == ''
    assert lines[1] == ''

    with pytest.raises(EOFError):
        file.load_lines(0, 3)

def test_file_with_two_lines_and_last_one_empty(generate_file_on_disk):
    file_path = generate_file_on_disk(content='foo\n')
    file = File(file_path)

    assert(file.number_of_lines == 2)
    assert file.number_of_bytes_in_longest_line == 3
    assert file.number_of_characters_in_longest_line == 3

    lines = file.load_lines(0, 1)
    assert len(lines) == 1
    assert lines[0] == 'foo'

    lines = file.load_lines(1, 1)
    assert len(lines) == 1
    assert lines[0] == ''

    lines = file.load_lines(0, 2)
    assert len(lines) == 2
    assert lines[0] == 'foo'
    assert lines[1] == ''

    with pytest.raises(EOFError):
        file.load_lines(0, 3)

def test_file_with_two_lines_and_first_one_empty(generate_file_on_disk):
    file_path = generate_file_on_disk(content='\nfoo')
    file = File(file_path)

    assert(file.number_of_lines == 2)
    assert file.number_of_bytes_in_longest_line == 3
    assert file.number_of_characters_in_longest_line == 3

    lines = file.load_lines(0, 1)
    assert len(lines) == 1
    assert lines[0] == ''

    lines = file.load_lines(1, 1)
    assert len(lines) == 1
    assert lines[0] == 'foo'

    lines = file.load_lines(0, 2)
    assert len(lines) == 2
    assert lines[0] == ''
    assert lines[1] == 'foo'

    with pytest.raises(EOFError):
        file.load_lines(0, 3)

def test_file_with_two_non_empty_lines(generate_file_on_disk):
    file_path = generate_file_on_disk(content='foo\nbar')
    file = File(file_path)

    assert(file.number_of_lines == 2)
    assert file.number_of_bytes_in_longest_line == 3
    assert file.number_of_characters_in_longest_line == 3

    lines = file.load_lines(0, 1)
    assert len(lines) == 1
    assert lines[0] == 'foo'

    lines = file.load_lines(1, 1)
    assert len(lines) == 1
    assert lines[0] == 'bar'

    lines = file.load_lines(0, 2)
    assert len(lines) == 2
    assert lines[0] == 'foo'
    assert lines[1] == 'bar'

    with pytest.raises(EOFError):
        file.load_lines(0, 3)

def test_file_with_three_empty_lines(generate_file_on_disk):
    file_path = generate_file_on_disk(content='\n\n')
    file = File(file_path)

    assert(file.number_of_lines == 3)
    assert file.number_of_bytes_in_longest_line == 0
    assert file.number_of_characters_in_longest_line == 0

    lines = file.load_lines(0, 1)
    assert len(lines) == 1
    assert lines[0] == ''

    lines = file.load_lines(1, 1)
    assert len(lines) == 1
    assert lines[0] == ''

    lines = file.load_lines(2, 1)
    assert len(lines) == 1
    assert lines[0] == ''

    lines = file.load_lines(0, 2)
    assert len(lines) == 2
    assert lines[0] == ''
    assert lines[1] == ''

    lines = file.load_lines(1, 2)
    assert len(lines) == 2
    assert lines[0] == ''
    assert lines[1] == ''

    lines = file.load_lines(0, 3)
    assert len(lines) == 3
    assert lines[0] == ''
    assert lines[1] == ''
    assert lines[2] == ''

    with pytest.raises(EOFError):
        file.load_lines(0, 4)

def test_file_with_three_lines_first_and_last_empty(generate_file_on_disk):
    file_path = generate_file_on_disk(content='\nfoo\n')
    file = File(file_path)

    assert(file.number_of_lines == 3)
    assert file.number_of_bytes_in_longest_line == 3
    assert file.number_of_characters_in_longest_line == 3

    lines = file.load_lines(0, 1)
    assert len(lines) == 1
    assert lines[0] == ''

    lines = file.load_lines(1, 1)
    assert len(lines) == 1
    assert lines[0] == 'foo'

    lines = file.load_lines(2, 1)
    assert len(lines) == 1
    assert lines[0] == ''

    lines = file.load_lines(0, 2)
    assert len(lines) == 2
    assert lines[0] == ''
    assert lines[1] == 'foo'

    lines = file.load_lines(1, 2)
    assert len(lines) == 2
    assert lines[0] == 'foo'
    assert lines[1] == ''

    lines = file.load_lines(0, 3)
    assert len(lines) == 3
    assert lines[0] == ''
    assert lines[1] == 'foo'
    assert lines[2] == ''

    with pytest.raises(EOFError):
        file.load_lines(0, 4)

def test_file_with_multibyte_character(generate_file_on_disk):
    file_path = generate_file_on_disk(content='👉 foo\n👉 bar baz')
    file = File(file_path)

    assert(file.number_of_lines == 2)
    assert file.number_of_bytes_in_longest_line == 12
    assert file.number_of_characters_in_longest_line == 9

    lines = file.load_lines(0, 1)
    assert len(lines) == 1
    assert lines[0] == '👉 foo'

    lines = file.load_lines(1, 1)
    assert len(lines) == 1
    assert lines[0] == '👉 bar baz'
