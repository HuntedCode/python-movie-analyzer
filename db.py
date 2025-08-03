from ast import literal_eval
import json
import os.path
import pandas as pd
import sqlite3

class Database:

    def __init__(self, movies_file='movies_metadata.csv', ratings_file='ratings.csv', db_file='movies.db'):
        """Initiate Database with movie data from CSV file."""

        self.db_file = db_file

        def parse_data(df: pd.DataFrame) -> pd.DataFrame:
            """Parses raw data into useable data for later filtering."""

            df['genres_parsed'] = df['genres'].apply(lambda x: literal_eval(x) if isinstance(x, str) and x.strip() else [])
            df['genres_list'] = df['genres_parsed'].apply(lambda x: [d['name'] for d in x] if isinstance(x, list) and x else [None])
            df['genres'] = df['genres_list'].apply(json.dumps)
            return df.drop(['genres_list', 'genres_parsed'], axis='columns')
        
        if not os.path.exists(db_file):
            print("Generating DB. Please wait...")
            conn = sqlite3.connect(db_file)

            movies_df = parse_data(pd.read_csv(movies_file, low_memory=False))
            movies_df.to_sql('movies', conn, if_exists='replace')
            
            ratings_df = pd.read_csv(ratings_file, low_memory=False)
            ratings_df.to_sql('ratings', conn, if_exists='replace')

            conn.close()
        else:
            print("DB Already Exists!")

    def _format_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """Formats data retrieved from db to allow easier manipulation later."""

        if 'genres' in df.columns:
            df['genres'] = df['genres'].apply(json.loads)

        return df
    
    def ratings_query_builder(self, left_table='movies', right_table='ratings', left_join_key='id', right_join_key='movieId', join_type='INNER', movie_id='862') -> tuple:
        return (f"""
        SELECT m.title, m.genres, r.userId, r.rating 
        FROM {left_table} m
        {join_type} JOIN {right_table} r
        ON m.{left_join_key} = r.{right_join_key}
        WHERE m.id = ?
        """, (movie_id,))

    def query_db(self, query: str="SELECT title, id, genres, vote_average FROM movies", limit: int=100) -> pd.DataFrame:
        """Queries Database without any user input. If wanting to use user set params, use query_db_with_params() instead."""

        if not "LIMIT" in query:
            query += f" LIMIT {limit}"

        conn = sqlite3.connect(self.db_file)
        df = pd.read_sql_query(query, conn)
        conn.close()

        return self._format_df(df)

    def query_db_with_params(self, query: str="SELECT title, genres, vote_average FROM movies WHERE vote_average > ?", params=(7.0,), limit: int=100) -> pd.DataFrame:
        """Queries Database using params to avoid SQL injection. Set limit=0 for no limit."""

        if not "LIMIT" in query and limit > 0:
            query += f" LIMIT {limit}"
            
        conn = sqlite3.connect(self.db_file)
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()

        return self._format_df(df)