from cli import cli_run
import db

if __name__ == "__main__":
    db_file = 'movies.db'
    db.init_db(csv_file='movies_metadata.csv', db_file=db_file, nrows=100, replace=False)
    df = db.query_db(db_file=db_file)
    cli_run(df)