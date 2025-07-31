from ast import literal_eval
import matplotlib.pyplot as plt
import os.path
import pandas as pd

accepted_commands = {"exit", "filter", "help", "load", "plot", "refresh", "save", "stats", "view"}

def cli_run(raw_df: pd.DataFrame):
    """Creates and runs basic CLI to access, filter and save/load movie data."""

    raw_df = parse_data(raw_df)
    filtered_df = raw_df

    while(True):
        command = input("What would you like to do?: ").lower()
        if command in accepted_commands:
            if command == "exit":
                break
            else:
                response_df = process_command(command, raw_df, filtered_df)
                if command == "load":
                    if not response_df is None:
                        raw_df = pd.concat([raw_df, response_df], ignore_index=True)
                        raw_df = raw_df.drop_duplicates(subset=['title'])

                        filtered_df = pd.concat([filtered_df, response_df], ignore_index=True)
                        filtered_df = filtered_df.drop_duplicates(subset=['title'])
                else:
                    filtered_df = response_df
        else:
            print("Invalid command, please try again.")

def parse_data(df: pd.DataFrame):
    """Parses raw data into useable data for later filtering."""

    df['genres_parsed'] = df['genres'].apply(lambda x: literal_eval(x) if isinstance(x, str) and x.strip() else [])
    df['genre_list'] = df['genres_parsed'].apply(lambda x: [d['name'] for d in x] if isinstance(x, list) and x else [None])
    return df.drop(['genres', 'genres_parsed'], axis='columns')

def process_command(command, raw_df: pd.DataFrame, filtered_df: pd.DataFrame):
    """Recieves and processes various command line commands."""

    match command:
        case "filter":
            return filter_command(raw_df)
        case "help":
            help_command()
        case "load":
            return load_command()
        case "plot":
            plot_command(filtered_df)
        case "refresh":
            return refresh_command(raw_df)
        case "save":
            save_command(filtered_df)
        case "stats":
            stats_command(filtered_df)
        case "view":
            view_command(filtered_df)
        
    return filtered_df

def filter_command(df: pd.DataFrame):
    """Filters incoming DataFrame based on user input and returns the result."""

    def get_genres():
        """Returns user input genres."""

        return str(input("Enter genre: ")).title().split()
    
    def get_ratings():
        """Returns user input min and max ratings."""

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
        return df
    
    view_command(filtered_df)
    return filtered_df

def help_command():
    """Dynamically outputs valid CLI commands."""

    string = "Use any of the following commands: "
    for index, command in enumerate(sorted(accepted_commands)):
        string += command
        if not index == len(accepted_commands) - 1:
            string += ", "
    print(string)

def load_command():
    """Returns loaded data from valid CSV/JSON file based on user input."""

    def check_file_exists(name):
        if os.path.isfile(name):
            return True
        else:
            print("That is not a valid file. Please try again.")
            return False

    filename = str(input("Enter file name: "))
    file_type = str(input("Enter file type to save. ('csv' or 'json'): ")).lower()

    try:
        if file_type in ('csv', 'c'):
            filename += '.csv'
            if check_file_exists(filename):
                df = pd.read_csv(filename)
                df['genre_list'] = df['genre_list'].apply(lambda x: literal_eval(x) if isinstance(x, str) and x.strip() else [])
            else:
                return None
        elif file_type in ('json', 'j'):
            filename += '.json'
            if check_file_exists(filename):
                df = pd.read_json(filename)
            else:
                return None
        else:
            print('Invalid file type. Please try again.')
            return None

        return df
    except pd.errors.ParserError:
        print("Error reading file. Check file integrity and try again.")

def plot_command(df: pd.DataFrame):
    ax = df.explode('genre_list').groupby('genre_list').size().plot(kind="bar")
    ax.set_title("Genre Counts")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Count")
    plt.tight_layout()

    plt.savefig('genres.png')
    print("Plot image saved successfully: genres.png")

def refresh_command(raw_df: pd.DataFrame):
    """Placeholder for more involved refresh command if needed. Currently just returns input df."""

    return raw_df

def save_command(df: pd.DataFrame):
    """Saves to valid CSV/JSON file based on user input."""

    def check_if_overwrite(name):
        if os.path.isfile(name):
            if not str(input("Would you like to overwrite this file? ('y'/'n'): ")).lower() == 'y':
                print("Please try again.")
                return False
        return True

    filename = str(input("Enter file name: "))
    file_type = str(input("Enter file type to save. ('csv' or 'json'): ")).lower()

    if file_type in ('csv', 'c'):
        filename += '.csv'
        if check_if_overwrite(filename):
            df.to_csv(filename)
    elif file_type in ('json', 'j'):
        filename += '.json'
        if check_if_overwrite(filename):
            df.to_json(filename)
    else:
        print('Invalid file type. Please try again.')
        
def stats_command(df: pd.DataFrame):
    """Prints basic genre and rating stats from incoming dataset."""

    flat = df.explode('genre_list')
    genre_counts = flat.groupby('genre_list').size()
    genre_means = flat.groupby('genre_list')['vote_average'].mean()
    print("\n", pd.DataFrame({'Count': genre_counts, 'Avg Rating': genre_means}), "\n")

def view_command(df: pd.DataFrame):
    """Prints dataset in an easy to read way."""

    print("\n", df[['title', 'genre_list', 'vote_average']].head(n=len(df)), "\n")