from db import Database
import matplotlib.pyplot as plt
import streamlit as st

if __name__ == "__main__":

    # init Database
    try:
        db = Database()
    except FileNotFoundError as inst:
        st.write("File could not be found. Make sure the file has been named properly and please try again.")
        st.write(inst)
    
    #Page Layout
    st.title("Movie Metadata Database")
    st.sidebar.header('Filters')

    #Load Full Data
    df = db.query_db(limit=0)

    #Sidebar Filters
    genre_input = st.sidebar.text_input("Genres (space-separated):")
    min_rating = st.sidebar.slider("Min Rating:", 0.0, 10.0, 0.0, 0.1)
    max_rating = st.sidebar.slider("Max Rating:", 0.0, 10.0, 10.0, 0.1)
    if len(genre_input) > 0:
        genres = str(genre_input).title().split()
    else:
        genres = []

    #Filter SQL Query
    params = []

    if len(genres) > 0 or min_rating > 0.0 or max_rating < 10.0:
        params = {'genres': genres, 'min_rating': min_rating, 'max_rating': max_rating}
        df = db.filter_query(opt_params=params)
    
    #Display Data
    st.header("Movie Data")
    st.dataframe(df)

    #Stats
    st.header("Stats")
    if st.button("Compute Stats"):
        if len(genres) > 0 or min_rating > 0.0 or max_rating < 10.0:
            opt_params = {'genres': genres, 'min_rating': min_rating, 'max_rating': max_rating}
            st.dataframe(db.genre_stats_query(opt_params=opt_params))
        else:
            st.dataframe(db.genre_stats_query())

    #Plot
    st.header("Genre Plot")
    if st.button("Generate Plot"):
        fig, ax = plt.subplots()
        if len(genres) > 0 or min_rating > 0.0 or max_rating < 10.0:
            opt_params = {'genres': genres, 'min_rating': min_rating, 'max_rating': max_rating}
            db.genre_stats_query(opt_params=opt_params).plot(kind='bar', x='genre', y='count', ax=ax)
        else:
            db.genre_stats_query().plot(kind='bar', x='genre', y='count', ax=ax)
        
        ax.set_title("Genre Counts")
        ax.set_xlabel("Genre")
        ax.set_ylabel("Count")
        plt.tight_layout()
        st.pyplot(fig)