import os.path
import pandas as pd
import sqlite3

class Database:

    def __init__(self, csv_file='movies_metadata.csv', db_file='movies.db', nrows=100, replace=False):
        """Initiate Database with movie data from CSV file."""

        self.db_file = db_file

        if replace or not os.path.exists(db_file):
            conn = sqlite3.connect(db_file)
            df = pd.read_csv(csv_file, nrows=nrows)
            df.to_sql('movies', conn, if_exists='replace', index=False)
            conn.close()

    def query_db(self, query="SELECT * FROM movies LIMIT 5") -> pd.DataFrame:
        """Queries Database without any user input. If wanting to use user set params, use query_db_with_params() instead."""

        conn = sqlite3.connect(self.db_file)
        df = pd.read_sql_query(query, conn)
        conn.close()

        return df

    def query_db_with_params(self, query="SELECT * FROM movies WHERE vote_average > ? LIMIT 5", params=(7.0,)) -> pd.DataFrame:
        """Queries Database using params to avoid SQL injection."""
        
        conn = sqlite3.connect(self.db_file)
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()

        return df