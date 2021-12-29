import sqlite3


def create():
    try:
        conn = sqlite3.connect('database/queries.db')
        conn.execute('CREATE TABLE IF NOT EXISTS URLS (url VARCHAR(30) UNIQUE,title varchar(30),metadesc varchar(300),contents VARCHAR(500))')
        conn.execute('CREATE VIRTUAL TABLE IF NOT EXISTS URLS_FTS USING FTS5(url,title,metadesc,contents)')
        conn.execute('Insert into URLS_FTS select * from URLS WHERE NOT EXISTS(SELECT * FROM URLS_FTS)')
        conn.commit()
        conn.close()
        print("Database Setup done!")

    except Exception as e:
        print(e)
        return
