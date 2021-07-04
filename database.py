# Desarrollado por:
# - Fuentes Rangel, Jesús Eduardo
# - López Barajas, Andrés Esaú
import click
from flask import g, current_app
from flask.cli import with_appcontext
from sqlalchemy import create_engine
from decouple import config

def create_db():
    database_connection = "{}://{}:{}@{}:{}/{}?charset=utf8".format(
            config('DB_DRIVER'),
            config('DB_USERNAME'),
            config('DB_PASSWORD'),
            config('DB_HOST'),
            config('DB_PORT'),
            config('DB_NAME'),
        )

    return create_engine(database_connection)

def get_db():
    if "db" not in g:
        g.db = create_db()

    return g.db

def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")

def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.cli.add_command(init_db_command)

