import os.path
import pandas as pd
import sqlite3

def init_db(csv_file='movies_metadata.csv', db_file='movies.db', nrows=100, replace=False) -> None:
    if replace or not os.path.exists(db_file):
        conn = sqlite3.connect(db_file)
        df = pd.read_csv(csv_file, nrows=nrows)
        df.to_sql('movies', conn, if_exists='replace', index=False)
        conn.close()

def query_db(db_file='movies.db', query='SELECT * FROM movies LIMIT 5') -> pd.DataFrame:
    conn = sqlite3.connect(db_file)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df