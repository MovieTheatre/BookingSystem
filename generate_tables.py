import sqlite3
VAR_DB_NAME = "movie.db"


def Create_Tables():
    connection = sqlite3.connect(VAR_DB_NAME)
    cursor = connection.cursor()

    create_tbl_movies = """
                        CREATE TABLE IF NOT EXISTS
                        Movies (id INTEGER PRIMARY KEY, name TEXT, rating REAL);"""

    create_tbl_projections = """
                        CREATE TABLE IF NOT EXISTS
                        Projections (id INTEGER PRIMARY KEY, movie_id INTEGER, type TEXT, projection_date NUMERIC, projection_time NUMERIC)
                        FOREIGN KEY(movie_id) REFERENCES Movies(id);"""

    create_tbl_reservations = """
                        CREATE TABLE IF NOT EXISTS
                        Reservations (id INTEGER PRIMARY KEY, username TEXT, projection_id TEXT, row INTEGER, col INTEGER)
                        FOREIGN KEY(projection_id) REFERENCES Projections(id);"""

    for sqlCommand in [create_tbl_movies, create_tbl_projections, create_tbl_reservations]:
        cursor.execute(sqlCommand)

Create_Tables()