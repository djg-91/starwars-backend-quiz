import typer

from ..utils import list_entities

planets_app = typer.Typer()


@planets_app.command('list')
def list_planets(
    page: int = typer.Option(1),
    page_size: int = typer.Option(10),
    search: str = typer.Option(None),
    sort_by: str = typer.Option(None),
    order: str = typer.Option('asc'),
):
    """List Star Wars planets."""
    list_entities(
        entity_name='Planets',
        endpoint='planets',
        columns=[
            'name',
            'rotation_period',
            'orbital_period',
            'diameter',
            'climate',
            'gravity',
            'terrain',
            'surface_water',
            'population',
        ],
        loading_message='Fetching planets from the API...',
        page=page,
        page_size=page_size,
        search=search,
        sort_by=sort_by,
        order=order,
    )
