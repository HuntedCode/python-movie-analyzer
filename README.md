# Enhanced Movie Ratings Dashboard

A Python-based tool for analyzing movie metadata and user ratings from Kaggle datasets. Features a command-line interface (CLI) for filtering, statistics, and visualizations, plus a Streamlit web dashboard for interactive exploration. Built as part of a 6-month self-taught Python career transition plan.

## Features
- **Data Loading**: Imports movie metadata (titles, genres, vote averages) and user ratings from CSV into SQLite for persistent storage.
- **Filtering**: SQL-based filters for genres (multi-genre OR matching), rating ranges, or both.
- **Statistics**: Genre-based counts and average ratings using SQL aggregations (json_each for multi-genres).
- **Ratings Query**: Fetch user ratings for a specific movie via SQL joins, with average calculation.
- **Visualizations**: Bar plots for genre counts, saved as PNG (Matplotlib).
- **Save/Load**: Export/import filtered data to/from CSV/JSON.
- **Web Dashboard**: Streamlit UI for dynamic filtering, data display, stats computation, and plotting.
- **Error Handling**: Robust checks for file existence, invalid inputs, NaN values, and parsing errors.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/HuntedCode/python-movie-analyzer.git
   cd python-movie-analyzer
   ```
2. Install dependencies (Python 3.8+ required):
   ```bash
   pip install pandas matplotlib streamlit
   ```
   (SQLite is built-in; no additional install needed.)
3. Download the datasets: Get `movies_metadata.csv` and `ratings.csv` from [Kaggle’s The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset). Place them in the project folder.

## Usage
### CLI Mode
Run the CLI for console-based interaction:
```bash
python main.py
```
- Commands: `view` (display data), `filter` (genre/rating), `stats` (genre averages/counts), `plot` (genre bar chart), `ratings` (user ratings per movie), `save`/`load` (CSV/JSON), `refresh` (reload data), `help`, `exit`.
- Example: Filter for "Drama" movies rated 7-9, compute stats, plot genres.

### Web Dashboard Mode
Run the Streamlit dashboard for browser-based use:
```bash
streamlit run app.py
```
- Opens at http://localhost:8501.
- Sidebar: Input genres (space-separated), slider for min/max rating.
- Main page: Displays filtered data table, buttons for stats (dataframe) and plot (bar chart).
- Example: Enter "Comedy Action", set ratings 8-10, click "Compute Stats" and "Generate Plot".

**Note**: For educational use. Respects Kaggle terms—use datasets responsibly.

## Project Structure
- `main.py`: CLI entry point.
- `app.py`: Streamlit dashboard entry point.
- `cli.py`: CLI commands and logic (filters, stats, plots).
- `db.py`: SQLite database management (loading, queries, joins, aggregations).
- `movies_metadata.csv` / `ratings.csv`: Kaggle input data (not in repo—download separately).

## Contributing
Feedback welcome! Fork the repo, make changes, and submit a pull request. Report issues on GitHub.

## License
MIT License—free to use and modify.

Built by Jeffrey Lowe as part of a 6-month Python learning plan for remote coding jobs. Last updated: August 5, 2025.