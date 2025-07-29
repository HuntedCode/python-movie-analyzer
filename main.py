from cli import cli_run
import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv('movies_metadata.csv', nrows=10)
    cli_run(df)