import typer

from ..utils import list_entities

people_app = typer.Typer()


@people_app.command('list')
def list_people(
    page: int = typer.Option(1),
    page_size: int = typer.Option(10),
    search: str = typer.Option(None),
    sort_by: str = typer.Option(None),
    order: str = typer.Option('asc'),
):
    """List Star Wars characters."""
    list_entities(
        entity_name='People',
        endpoint='people',
        columns=[
            'name',
            'height',
            'mass',
            'hair_color',
            'skin_color',
            'eye_color',
            'birth_year',
            'gender',
        ],
        loading_message='Fetching people from the API...',
        page=page,
        page_size=page_size,
        search=search,
        sort_by=sort_by,
        order=order,
    )
