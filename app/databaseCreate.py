import sqlite3


def create():
    try:
        conn = sqlite3.connect('database/queries.db')
        conn.execute('CREATE TABLE URLS (url VARCHAR(30) UNIQUE,title varchar(30),metadesc varchar(300),contents VARCHAR(500))')
        conn.close()

    except Exception as e:
        print(e)
        return
