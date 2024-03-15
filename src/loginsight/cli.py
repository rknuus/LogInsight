from loginsight.app import InteractiveLogViewer
from loginsight.file import File
import click


@click.command()
@click.argument("filepath", type=click.Path(exists=True))
def run(filepath):
    file = File(filepath)
    app = InteractiveLogViewer(file)
    app.run()
