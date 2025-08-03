from db import Database
import matplotlib.pyplot as plt
import os.path
import pandas as pd

accepted_commands = {"exit", "filter", "help", "plot", "ratings", "refresh", "save", "stats", "view"}

def cli_run(db: Database) -> None:
    """Creates and runs basic CLI to access, filter and save/load movie data."""

    cache_df = db.query_db()

    while(True):
        command = input("What would you like to do?: ").lower()
        if command in accepted_commands:
            if command == "exit":
                break
            else:
                cache_df = process_command(command, db, cache_df)
        else:
            print("Invalid command, please try again.")

def process_command(command, db: Database, cache_df: pd.DataFrame) -> pd.DataFrame:
    """Recieves and processes various command line commands."""

    match command:
        case "filter":
            return filter_command(db)
        case "help":
            help_command()
        case "plot":
            plot_command(db, cache_df)
        case "ratings":
            ratings_command(db)
        case "refresh":
            return refresh_command(db)
        case "save":
            save_command(cache_df)
        case "stats":
            stats_command(db, cache_df)
        case "view":
            view_command(cache_df)
        
    return cache_df

def filter_command(db: Database) -> pd.DataFrame:
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

    query_str = "SELECT * FROM movies WHERE EXISTS ("
    params = []

    if type in ('genre', 'g', 'both', 'b'):
        genres = get_genres()
        query_str += "SELECT 1 FROM json_each(genres) WHERE "
        pos = -1
        for g in genres:
            pos += 1
            query_str += "value = ?"
            params.append(g)
            if pos < len(genres) - 1:
                query_str += " OR "
            else:
                query_str += ")"
        
        if type in ('both', 'b'):
            query_str += " AND ("

    if type in ('rating', 'r', 'both', 'b'):
        rating_min, rating_max = get_ratings()
        query_str += "vote_average BETWEEN ? AND ?)"
        params.append(rating_min)
        params.append(rating_max)
    
    if len(params) >= 1:
        df = db.query_db_with_params(query_str, params)
        view_command(df)
        return df
    else:
        print("That is not a valid command, please try again.")
        return refresh_command(db)

def help_command() -> None:
    """Dynamically outputs valid CLI commands."""

    string = "Use any of the following commands: "
    for index, command in enumerate(sorted(accepted_commands)):
        string += command
        if not index == len(accepted_commands) - 1:
            string += ", "
    print(string)

def plot_command(db: Database, cache_df: pd.DataFrame) -> None:
    input_str = str(input("Use filtered data (f) or full dataset (full)? "))

    if input_str == 'f':
        ax = cache_df.explode('genres').groupby('genres').size().plot(kind="bar")
    elif input_str == 'full':
        query_str = "SELECT value AS genre, COUNT(*) AS count FROM movies, json_each(genres) GROUP BY value"
        ax = db.query_db(query_str).plot(kind="bar", x='genre', y='count')
    else:
        print("That is not a valid command. Please try again!")
        return

    ax.set_title("Genre Counts")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Count")
    plt.tight_layout()

    plt.savefig('genres.png')
    print("Plot image saved successfully: genres.png")

def ratings_command(db: Database) -> None:
    print("Get user ratings for specified movie.")

    try:
        movie_id = int(input("Enter movie id: "))
    except ValueError:
        print("That is not a valid movie id! Must be an integer.")
        return

    sql, params = db.ratings_query_builder(movie_id=movie_id)
    df = db.query_db_with_params(sql, params, 0)
    title = df['title'].iloc[0]
    genres = df['genres'].iloc[0]
    average = df['rating'].mean()

    print("User ratings (0.0 - 5.0) for:")
    print(f"\nTitle: {title} | Genres: {genres}\n")
    print(df[['userId', 'rating']])
    print(f"\nAvearge rating: {average}")

def refresh_command(db: Database) -> pd.DataFrame:
    """Placeholder for more involved refresh command if needed. Currently just returns input df."""

    return db.query_db()

def save_command(df: pd.DataFrame) -> None:
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
        
def stats_command(db: Database, cache_df: pd.DataFrame) -> None:
    """Prints basic genre and rating stats from incoming dataset."""

    input_str = str(input("Use filtered data (f) or full dataset (full)? "))
    if input_str == 'f':
        flat = cache_df.explode('genres')
        genre_counts = flat.groupby('genres').size()
        genre_means = flat.groupby('genres')['vote_average'].mean()
        print("\n", pd.DataFrame({'Count': genre_counts, 'Avg Rating': genre_means}), "\n")
    elif input_str == "full":
        query_str = "SELECT value AS genre, COUNT(*) AS count, AVG(vote_average) as avg FROM movies, json_each(genres) GROUP BY value"
        cache_df = db.query_db(query_str)
        print(cache_df)
    else:
        print("That is not a valid command. Please try again.")

def view_command(df: pd.DataFrame) -> None:
    """Prints dataset in an easy to read way."""

    print("\n", df, "\n")