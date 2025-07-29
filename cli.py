from ast import literal_eval
import pandas as pd

accepted_commands = {"exit", "filter", "help", "stats", "view"}

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
    df['genre_list'] = df['genres_parsed'].apply(lambda x: [d['name'] for d in x] if isinstance(x, list) and x else [None])
    df.drop('genres_parsed', axis='columns')

def process_command(command, df: pd.DataFrame):
    match command:
        case "filter":
            filter_command(df)
        case "help":
            help_command()
        case "stats":
            stats_command(df)
        case "view":
            view_command(df)

def filter_command(df: pd.DataFrame):

    def get_genres():
        return str(input("Enter genre: ")).title().split()
    
    def get_ratings():
        while(True):
            try:
                rating_min = float(input("Enter minimum rating: "))
            except ValueError:
                print("Please enter a vald number!")
            else:
                break
            
        while(True):
            while(True):
                try:        
                    rating_max = float(input("Enter maximum rating: "))
                except ValueError:
                    print("Please enter a vald number!")
                else:
                    break
            if rating_max >= rating_min:
                break
            print(f"Please enter greater than or equal to {rating_min}")
        
        return rating_min, rating_max
        

    type = str(input("What would you like to filter? ('genre', 'rating' or 'both'): ")).lower()

    if type in ('genre', 'g'):
        genres = get_genres()
        filtered_df = df[df['genre_list'].apply(lambda x: any(g in x for g in genres))]
    elif type in ('rating', 'r'):
        rating_min, rating_max = get_ratings()
        filtered_df = df[(df['vote_average'] >= rating_min) & (df['vote_average'] <= rating_max)]
    elif type in ('both', 'b'):
        genres = get_genres()
        rating_min, rating_max = get_ratings()
        filtered_df = df[
            (df['vote_average'] >= rating_min) & 
            (df['vote_average'] <= rating_max) &
            df['genre_list'].apply(lambda x: any(g in x for g in genres))]
    else:
        print("Invalid filter. Please try again.")
        return
    
    view_command(filtered_df)

def help_command():
    string = "Use any of the following commands: "
    for index, command in enumerate(sorted(accepted_commands)):
        string += command
        if not index == len(accepted_commands) - 1:
            string += ", "
    print(string)

def stats_command(df: pd.DataFrame):
    print("\nMean vote average: ", df['vote_average'].mean())
    print("Total vote averages: ", df['vote_average'].count(), "\n")

def view_command(df: pd.DataFrame):
    print("\n", df[['title', 'genre_list', 'vote_average']].head(n=len(df)), "\n")