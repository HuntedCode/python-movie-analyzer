from ast import literal_eval
import json
import os
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

            try:
                movies_df = parse_data(pd.read_csv(movies_file, low_memory=False))
                movies_df.to_sql('movies', conn, if_exists='replace')
                
                ratings_df = pd.read_csv(ratings_file, low_memory=False)
                ratings_df.to_sql('ratings', conn, if_exists='replace')
            except FileNotFoundError:
                conn.close()
                os.remove(db_file)
                raise

            conn.close()
        else:
            print("DB Already Exists!")

    def _filter_sql_builder(self, input_params: dict) -> tuple:
        """Builds filter string that can be appended easily to any SQL statement."""

        params = []

        if 'genres' in input_params:
            placeholders = ", ".join("?" for _ in input_params['genres'])
            num_genres = len(input_params['genres'])
            sql = f""" 
                WHERE (
                    SELECT COUNT(DISTINCT value)
                    FROM json_each(genres)
                    WHERE value IN ({placeholders})
                ) >= {num_genres}
                """
            for g in input_params['genres']:
                params.append(g)

            if ('min_rating' in input_params and input_params['min_rating'] > 0.0) or ('max_rating' in input_params and input_params['max_rating'] < 10.0):
                sql += " AND "
        
        if ('min_rating' in input_params and input_params['min_rating'] > 0.0) or ('max_rating' in input_params and input_params['max_rating'] < 10.0):
            sql += "(vote_average >= ? AND vote_average <= ?)"
            params.append(input_params['min_rating'])
            params.append(input_params['max_rating'])
        
        return (sql, params,)

    def _format_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """Formats data retrieved from db to allow easier manipulation later."""

        if 'genres' in df.columns:
            df['genres'] = df['genres'].apply(json.loads)
        
        if 'vote_average' in df.columns:
            df = df.dropna(subset=['vote_average'])

        return df

    def filter_query(self, table='movies', limit=0, opt_params={}) -> pd.DataFrame:
        """Easy to use query to filter dataset quickly. Returns DataFrame."""

        sql = "SELECT title, id, genres, vote_average FROM movies"
        filter_str, params = self._filter_sql_builder(opt_params)
        return self.query_db_with_params(sql + filter_str, params, limit)

    def genre_stats_query(self, table='movies', limit=0, opt_params={}) -> pd.DataFrame:
        """Easy to use query to get stats information quickly. Returns DataFrame."""

        sql = f"SELECT value AS genre, COUNT(*) AS count, AVG(vote_average) AS avg FROM {table}, json_each(genres)"

        if len(opt_params) > 0:
            filter_str, params = self._filter_sql_builder(opt_params)
            sql += filter_str + " GROUP BY value"
            return self.query_db_with_params(sql, params, limit)

        sql += " GROUP BY value"
        return self.query_db(sql, limit=limit)

    def ratings_query(self, left_table='movies', right_table='ratings', left_join_key='id', right_join_key='movieId', join_type='INNER', movie_id='862', limit=0) -> pd.DataFrame:
        """Easy to use query to get ratings information quickly. Returns DataFrame."""

        return self.query_db_with_params(f"""
        SELECT m.title, m.id, m.genres, r.userId, r.rating, AVG(r.rating) OVER() as avg
        FROM {left_table} m
        {join_type} JOIN {right_table} r
        ON m.{left_join_key} = r.{right_join_key}
        WHERE m.id = ?
        """, (movie_id,), limit)

    def query_db(self, sql: str="SELECT title, id, genres, vote_average FROM movies", limit: int=100) -> pd.DataFrame:
        """Queries Database without any user input. If wanting to use user set params, use query_db_with_params() instead."""

        if not "LIMIT" in sql and limit > 0:
            sql += f" LIMIT {limit}"

        conn = sqlite3.connect(self.db_file)
        df = pd.read_sql_query(sql, conn)
        conn.close()

        return self._format_df(df)

    def query_db_with_params(self, sql: str="SELECT title, genres, vote_average FROM movies WHERE vote_average > ?", params=(7.0,), limit: int=100) -> pd.DataFrame:
        """Queries Database using params to avoid SQL injection. Set limit=0 for no limit."""

        if not "LIMIT" in sql and limit > 0:
            sql += f" LIMIT {limit}"
            
        conn = sqlite3.connect(self.db_file)
        df = pd.read_sql_query(sql, conn, params=params)
        conn.close()

        return self._format_df(df)