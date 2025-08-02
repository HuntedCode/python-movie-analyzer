from cli import cli_run
from db import Database

if __name__ == "__main__":

    db = Database()
    cli_run(db)