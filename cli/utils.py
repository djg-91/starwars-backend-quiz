import json
from contextlib import contextmanager
from typing import Any

import httpx
import typer
from decouple import config as env
from rich.box import ROUNDED
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


def render_table(title: str, data: list[dict], columns: list[str]) -> None:
    """
    Render a Rich table in the terminal.

    Args:
        title (str): Table title.
        data (list[dict]): Data rows.
        columns (list[str]): List of column keys to display.
    """

    def display(value: Any) -> str:
        """Render cell values, replacing None with '---'."""
        return str(value) if value is not None else '---'

    table = Table(title=title, show_lines=True, box=ROUNDED)

    for column in columns:
        table.add_column(column.replace('_', ' ').title(), no_wrap=False, overflow='fold')

    for item in data:
        row = [display(item.get(col)) for col in columns]
        table.add_row(*row)

    console.print(table)


@contextmanager
def clean_status(message: str, spinner: str = 'aesthetic'):
    """
    Context manager that shows a loading spinner and clears it on exit.

    Args:
        message (str): Loading message.
        spinner (str): Spinner style (default: 'aesthetic').
    """
    status = console.status(message, spinner=spinner)
    status.start()
    try:
        yield
    finally:
        status.stop()
        console.print(' ' * console.width, end='\r')  # Clear line


def show_error(message: str, code: int) -> None:
    """
    Display a formatted error message and exit the CLI.

    Args:
        message (str): Error text.
        code (int): Exit code.
    """
    text = Text(message)
    panel = Panel(
        text,
        title=Text('Error', style='red'),
        title_align='left',
        border_style='red',
    )
    console.print(panel)
    raise typer.Exit(code=code)


def handle_http_error(exc: httpx.HTTPStatusError, code: int) -> None:
    """
    Handle HTTP errors and show detailed API response if available.

    Args:
        exc (HTTPStatusError): Raised exception.
        code (int): Exit code.
    """
    try:
        error_json = exc.response.json()
        formatted = json.dumps(error_json, indent=2)
        message = f'API error: {exc.response.status_code}\n{formatted}'
    except Exception:
        message = f'API error: {exc.response.status_code} {exc.response.text}'
    show_error(message, code)


def safe_get(url: str, params: dict[str, Any]) -> dict[str, Any] | None:
    """
    Safely perform an HTTP GET request with error handling.

    Args:
        url (str): Full API URL.
        params (dict): Query parameters.

    Returns:
        dict | None: Response JSON or None on error.
    """
    try:
        response = httpx.get(url, params=params, timeout=5.0)
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        show_error(f'Connection error: {e}', code=1)
    except httpx.HTTPStatusError as e:
        handle_http_error(e, 2)


def list_entities(
    entity_name: str,
    endpoint: str,
    columns: list[str],
    loading_message: str,
    page: int,
    page_size: int,
    search: str | None,
    sort_by: str | None,
    order: str,
):
    """
    Generic CLI handler to list SWAPI resources.

    Args:
        entity_name (str): table title (e.g., People, Planets).
        endpoint (str): API endpoint to hit.
        columns (list[str]): columns to display in the table.
        loading_message (str): spinner message.
        page (int): page number (1-based).
        page_size (int): number of results per page.
        search (str): optional name-based filter.
        sort_by (str): optional attribute to sort by.
        order (str): asc or desc (default asc).
    """
    params = {
        'page': page,
        'page_size': page_size,
        'search': search,
        'sort_by': sort_by,
        'order': order,
    }

    params = {k: v for k, v in params.items() if v is not None}

    with clean_status(loading_message):
        data = safe_get(f'{env("INTERNAL_API_BASE_URL")}/{endpoint}/', params)

    if data:
        render_table(entity_name, data['results'], columns)
