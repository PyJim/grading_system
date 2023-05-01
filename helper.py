import sqlite3
from flask import g

DATABASE_FILE = 'database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_FILE)
        db.row_factory = sqlite3.Row
    return db

# return the results from a database query


def db_query(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# execute a statement on the database


def db_execute(query, args=()):
    conn = get_db()
    conn.execute(query, args)
    conn.commit()
    #conn.close()
