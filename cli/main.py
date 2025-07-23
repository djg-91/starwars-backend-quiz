import typer

from cli.commands.people import people_app
from cli.commands.planets import planets_app

app = typer.Typer()

app.add_typer(people_app, name='people')
app.add_typer(planets_app, name='planets')

if __name__ == '__main__':
    app()
