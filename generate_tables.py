import sqlite3
VAR_DB_NAME = "movie.db"


def delete_tables():

    connection = sqlite3.connect(VAR_DB_NAME)
    cursor = connection.cursor()

    tables = ["Movies", "Projections", "Reservations"]

    for table in tables:
        cursor.execute("DROP TABLE IF EXISTS {};".format(table))

    connection.commit()

    cursor.close()
    connection.close()


def create_tables():

    connection = sqlite3.connect(VAR_DB_NAME)
    cursor = connection.cursor()

    createMovies = """
                   CREATE TABLE IF NOT EXISTS
                   Movies (id INTEGER PRIMARY KEY,
                            name TEXT,
                            rating REAL);
                   """

    createProjections = """
                        CREATE TABLE IF NOT EXISTS
                        Projections (id INTEGER PRIMARY KEY,
                                    movie_id INTEGER,
                                    type TEXT,
                                    projection_date TEXT,
                                    projection_time TEXT,
                        FOREIGN KEY(movie_id) REFERENCES Movies(id));
                        """

    createReservations = """
                        CREATE TABLE IF NOT EXISTS
                        Reservations (id INTEGER PRIMARY KEY,
                                      username TEXT,
                                      projection_id TEXT,
                                      row INTEGER,
                                      col INTEGER,
                        FOREIGN KEY(projection_id) REFERENCES Projections(id));
                        """

    for sqlCommand in [createMovies, createProjections, createReservations]:
        cursor.execute(sqlCommand)

    connection.commit()

    cursor.close()
    connection.close()


def fill_movies_and_projections():

    connection = sqlite3.connect(VAR_DB_NAME)
    cursor = connection.cursor()

    tupleMovies = [
        ("The Hunger Games: Catching Fire", 7.9),
        ("Wreck-It Ralph", 7.8),
        ("Her", 8.3),
    ]

    tupleProjections = [
        (1, "3D", "2014-04-01", "19:10"),
        (1, "2D", "2014-04-01", "19:00"),
        (1, "4DX", "2014-04-02", "21:00"),
        (3, "2D", "2014-04-05", "20:20"),
        (2, "3D", "2014-04-02", "22:00"),
        (2, "2D", "2014-04-02", "19:30"),
    ]

    insertMovies = """
                    INSERT INTO Movies(name, rating)
                    VALUES(?, ?)
                   """

    insertProjections = """
                        INSERT INTO Projections(movie_id, type, projection_date, projection_time)
                        VALUES(?, ?, ?, ?)
                        """

    for movie in tupleMovies:
        cursor.execute(insertMovies, (movie[0], movie[1]))

    for projection in tupleProjections:
        cursor.execute(insertProjections, (projection[0], projection[1], projection[2], projection[3]))

    connection.commit()
    cursor.close()
    connection.close()


delete_tables()
create_tables()
fill_movies_and_projections()
