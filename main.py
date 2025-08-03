from cli import cli_run
from db import Database

if __name__ == "__main__":

    try:
        db = Database()
        cli_run(db)
    except FileNotFoundError as inst:
        print("File could not be found. Make sure the file has been named properly and please try again.")
        print(inst)