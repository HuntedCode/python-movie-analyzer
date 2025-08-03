# Movie Ratings Analyzer CLI

A command-line tool for analyzing movie data from a Kaggle dataset, allowing users to filter, compute statistics, save/load results, and visualize genre trends. Built in Python as part of a self-taught career transition to remote data or backend roles.

## Features
- Load and parse movie data (titles, genres, ratings) from CSV/JSON files.
- Filter movies by genre, rating range, or both (multi-genre support with OR logic).
- Compute stats: Per-genre averages/counts.
- Save filtered results to CSV/JSON and load back for further analysis.
- Visualize genre counts as bar charts (saved as PNG).
- Robust error handling for invalid files and user inputs.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/HuntedCode/python-movie-analyzer.git
   cd python-movie-analyzer
   ```
2. Install dependencies (Python 3.8+ required):
   ```bash
   pip install pandas matplotlib
   ```
3. Download the dataset: Use `movies_metadata.csv` from [Kaggle’s The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset) and place it in the project folder.

## Usage
Run the app from the command line:
```bash
python main.py
```

Available commands:
- `view`: Display current dataset (title, genres, rating).
- `filter`: Filter by genre (e.g., “Comedy Drama”), rating range (e.g., 7-9), or both.
- `stats`: Show mean rating, total ratings, and genre-based counts/averages.
- `save`: Export current dataset to CSV/JSON (prompts for format).
- `load`: Import CSV/JSON to append to current dataset.
- `refresh`: Reset to original dataset (placeholder for future reload).
- `plot`: Generate and save a bar chart of genre counts (genres.png).
- `help`: List all commands.
- `exit`: Quit the app.

Example session:
1. Run `python main.py` to load movies_metadata.csv.
2. `filter` by “Comedy” or ratings “7 to 9”.
3. `stats` to see genre averages.
4. `save` to “movies_filtered.csv”.
5. `plot` to generate genres.png.
6. `view` to check results.

**Note**: For educational use only. Respects Kaggle’s dataset terms.

## Project Structure
- `main.py`: Entry point, loads CSV and starts CLI.
- `cli.py`: Handles user interface, commands, and data processing (Pandas).

## Contributing
Feedback welcome! Fork the repo, make changes, and submit a pull request. Report issues on GitHub.

## License
MIT License—free to use and modify.

Built by Jeffrey Lowe as part of a 6-month Python learning plan for remote coding jobs. Last updated: July 31, 2025.