import flask
import sqlite3
import pathlib

app = flask.Flask(__name__)
ROOT = pathlib.Path(__file__).resolve().parent.parent
DATABASE_FILENAME = ROOT/'sql'/'newscrawler.sqlite3'
app.secret_key = 'Annatator'


def get_db():
  """Open a new database connection.

  Flask docs:
  https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
  """
  if 'sqlite_db' not in flask.g:
    flask.g.sqlite_db = sqlite3.connect(str(DATABASE_FILENAME))

    # Foreign keys have to be enabled per-connection.  This is an sqlite3
    # backwards compatibility thing.
    flask.g.sqlite_db.execute("PRAGMA foreign_keys = ON")
  return flask.g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Close the database at the end of a request.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    assert error or not error  # Needed to avoid superfluous style error
    sqlite_db = flask.g.pop('sqlite_db', None)
    if sqlite_db is not None:
        sqlite_db.commit()
        sqlite_db.close()