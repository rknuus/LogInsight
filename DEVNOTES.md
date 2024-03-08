## ideas

- create database from parsed file to speed up querying
- check out https://lnav.org/ as well as toolong

## Notes to myself:

- run `textual console` in a console
- run `rye run textual run --dev src/toolong_tui/demo.py` in another console (both consoles require `. .venv/bin/activate.fish`)
- to test: `rye run pytest`
- to run a single test: `rye run pytest -k test_requesting_one_line_returns_line`
- to open the debugger for a failed test: `rye run pytest --pdb`
- to generate a test coverage report: `rye run pytest --cov=toolong_tui --cov-context=test --cov-report=html test/`
- to test the type annotations: `rye run mypy src/toolong_tui/file.py`