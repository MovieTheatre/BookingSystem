import sqlite3


VAR_DB_NAME = "movie.db"
TABLES = ["Movies", "Projections", "Reservations"]


def show_movies():

    connection = sqlite3.connect(VAR_DB_NAME)
    cursor = connection.cursor()
    connection.row_factory = sqlite3.Row

    cursor.execute("SELECT id, name, rating FROM Movies")

    rows = cursor.fetchall()
    for row in rows:
        print("[{}] - {} ({})".format(row[0], row[1], row[2]))

    cursor.close()
    connection.close()


def show_movie_projections(movieId):

    connection = sqlite3.connect(VAR_DB_NAME)
    cursor = connection.cursor()
    connection.row_factory = sqlite3.Row

    cursor.execute("SELECT name FROM movies WHERE id = ? ;", (movieId, ))
    movieName = cursor.fetchone()[0]

    cursor.execute("""
                    SELECT id, projection_date, projection_time, type
                    FROM Projections
                    WHERE movie_id = ?
                   """, (movieId,))

    movieProjections = cursor.fetchall()

    print("Projections for movie '{}':".format(movieName))
    for row in movieProjections:
        print("[{}] - {} {} ({})".format(row[0], row[1], row[2], row[3]))

    cursor.close()
    connection.close()


def make_reservation():

    connection = sqlite3.connect(VAR_DB_NAME)
    cursor = connection.cursor()
    connection.row_factory = sqlite3.Row

    userName = input("Choose name> ")
    numberTickets = int(input("Choose number of tickets> "))
    print("Current movies:")
    show_movies()
    movieChoice = input("Choose a movie> ")
    show_movie_projections(movieChoice)
    projectionChoice = input("Choose a projection>")

    taken = get_taken_seats(projectionChoice)
    generate_projection_map(taken)

    booked_seats = get_seats(numberTickets)

    insertProjections = """
                        INSERT INTO Reservations(username, projection_id, row, col)
                        VALUES(?, ?, ?, ?)
                        """

    for seat in booked_seats:
        cursor.execute(
            insertProjections, (userName, projectionChoice, seat[0], seat[1]))
    connection.commit()

    taken = get_taken_seats(projectionChoice)
    generate_projection_map(taken)

    cursor.close()
    connection.close()


def get_taken_seats(projection_id):
    connection = sqlite3.connect(VAR_DB_NAME)
    cursor = connection.cursor()
    connection.row_factory = sqlite3.Row

    taken = []

    getTaken = """SELECT row, col
                  FROM Reservations
                  WHERE projection_id = ?
              """
    cursor.execute(getTaken, (projection_id, ))
    connection.commit()

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def generate_projection_map(taken):

    # header numbers
    for col in range(1, 11):
        if col == 1:
            print("  ", end=" ")

        print(col, end=" ")
        if col == len(range(1, 11)):
            print()

    # row numbers
    for row in range(1, 11):
        for col in range(1, 11):
            if col == 1:
                if row == 10:
                    print(row, end=" ")
                else:
                    print(row, end="  ")
            # seats
            if (row, col) in taken:
                print("X", end=" ")

            else:
                print(".", end=" ")
            if col == len(range(1, 11)):
                print()


def get_seats(numberTickets):
    seatMatrix = []
    for x in range(1, numberTickets + 1):
        seat = input("Choose seat {}>".format(x)).strip("(){}<>")
        seatRC = seat.split(",")
        row = seatRC[0]
        col = seatRC[1]
        seatMatrix.append([row, col])
    return seatMatrix


make_reservation()
