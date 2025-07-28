import pandas as pd

if __name__ == "__main__":
    df = pd.DataFrame(pd.read_csv('movies_metadata.csv', nrows=5))
    print(df.head())