import click

from dolt import app, db
from dolt.models import Courier, Customer, Employee, Partner


@app.cli.command()
def mock():
    pass
