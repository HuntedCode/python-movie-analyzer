from ast import literal_eval
import pandas as pd

accepted_commands = {"exit", "stats", "view"}

def cli_run(df: pd.DataFrame):
    parse_data(df)

    while(True):
        command = input("What would you like to do?: ").lower()
        if command in accepted_commands:
            if command == "exit":
                break
            else:
                process_command(command, df)
        else:
            print("Invalid command, please try again.")

def parse_data(df: pd.DataFrame):
    df['genres_parsed'] = df['genres'].apply(lambda x: literal_eval(x) if isinstance(x, str) and x.strip() else [])
    df['first_genre'] = df['genres_parsed'].apply(lambda x: x[0]['name'] if len(x) > 0 else None)

def process_command(command, df: pd.DataFrame):
    match command:
        case "stats":
            stats_command(df)
        case "view":
            view_command(df)

def stats_command(df: pd.DataFrame):
    print("\nMean vote average: ", df['vote_average'].mean())
    print("Total vote averages: ", df['vote_average'].count(), "\n")

def view_command(df: pd.DataFrame):
    print(df[['title', 'first_genre', 'vote_average']].head(n=10))