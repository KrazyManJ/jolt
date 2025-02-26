import sqlite3
import os
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        project_root = os.path.dirname(os.path.realpath(__file__))
        database_path = os.path.join(project_root, '..', current_app.config['DATABASE'])
        g.db = sqlite3.connect(
            database_path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

        # g.db.set_trace_callback(print)
        g.db.execute("PRAGMA foreign_keys = ON;")
        g.db.commit()

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('database/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
