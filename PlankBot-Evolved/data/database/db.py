from os.path import isfile
from sqlite3 import connect

DB_PATH = r"data/database/database.db"
SQL_PATH = r"data/database/start.sql"

conn = connect(DB_PATH, check_same_thread=False, isolation_level=None)

curs = conn.cursor()

def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()

    return inner

@with_commit
def build():
    if isfile(SQL_PATH):
        scriptexec(SQL_PATH)


def commit():
    conn.commit()


def close():
    conn.close()


def field(command : str, *values):
    curs.execute(command, tuple(values))

    if (fetch := curs.fetchone()) is not None:
        return fetch[0]


def record(command : str, *values):
    curs.execute(command, tuple(values))

    return curs.fetchone()
    

def records(command : str, *values):
    curs.execute(command, tuple(values))

    return curs.fetchall()


def column(command : str, *values):
    curs.execute(command, tuple(values))

    return [item[0] for item in curs.fetchall()]


def execcommit(command : str, *values):
    curs.execute(command, tuple(values))
    commit()


def execute(command : str, *values):
    curs.execute(command, tuple(values))


def multiexec(command : str, valueSet):
    curs.executemany(command, valueSet)


def scriptexec(path : str):
    with open(path, encoding="utf-8") as f:
        curs.executescript(f.read())
