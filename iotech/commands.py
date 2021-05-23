import click
from flask.cli import with_appcontext

from iotech.extensions import db
from iotech.models import User

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()