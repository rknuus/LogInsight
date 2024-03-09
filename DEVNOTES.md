## ideas

- create database from parsed file to speed up querying
- check out https://lnav.org/ as well as toolong

## Notes to myself:

### Run
- run `rye run textual run <script>` in another console (both consoles require `. .venv/bin/activate.fish`)

### Test
- to test: `rye run pytest`
- to run a single test: `rye run pytest -k test_requesting_one_line_returns_line`
- to open the debugger for a failed test: `rye run pytest --pdb`
- to generate a test coverage report: `rye run pytest --cov=toolong_tui --cov-context=test --cov-report=html test/`
- to test the type annotations: `rye run mypy src/toolong_tui/file.py`

### Debug
- add `self.log('foo', bar)` in an `App` or a `Widget` (see https://textual.textualize.io/guide/devtools/#textual-log)
- run `textual console` in a console
- run `rye run textual run --dev src/loginsight/main.py src/loginsight/main.py` in another console (both consoles require `. .venv/bin/activate.fish`)
