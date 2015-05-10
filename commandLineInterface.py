import sqlite3
from settings import *


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
    booked_seats = False

    while not booked_seats:
        booked_seats = get_seats(numberTickets, taken)

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

    reservationData(projectionChoice, booked_seats, userName)

    cursor.close()
    connection.close()


def reservationData(projection_id, booked_seats, userName):
    connection = sqlite3.connect(VAR_DB_NAME)
    cursor = connection.cursor()
    connection.row_factory = sqlite3.Row

    sql = """
            SELECT
            movies.name, movies.rating, projections.type, projections.projection_date, projections.projection_time
            FROM projections
            INNER JOIN movies
            ON projections.movie_id = movies.id
            WHERE projections.id = ?
            """
    cursor.execute(sql, (projection_id))

    result = cursor.fetchall()

    movieName = result[0][0]
    movieDate = result[0][3]
    movieTime = result[0][4]
    movieType = result[0][2]
    movieRanking = result[0][1]

    print("This is your reservation:")
    print("Movie: {} {}".format(movieName, movieRanking))
    print("Date and Time {} {} {}".format(movieDate, movieTime, movieRanking))
    print("Seats: {}".format(booked_seats))
    finalization = input("Enter finalize to finalize> ")
    if finalization == "finalize":
        print(CONFIRM_RESERVATION_PIC)
    else:
        cancel_reservation(userName)
        print(CANCEL_RESERVATION_PIC)


def cancel_reservation(userName):
    connection = sqlite3.connect(VAR_DB_NAME)
    cursor = connection.cursor()

    sql = """DELETE FROM reservations
      WHERE userName = ? ;
      """

    cursor.execute(sql, (userName,))
    connection.commit()


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


def check_if_seat_is_taken(row, col, seatMatrix, taken):
    if ((row, col) in seatMatrix) or (row, col) in taken:
        return True
    return False


def get_seats(numberTickets, taken):
    seatMatrix = []

    for x in range(1, numberTickets + 1):

        seat = input("Choose seat {}>".format(x)).strip("(){}<>")
        seatRC = seat.split(",")

        row = int(seatRC[0])
        col = int(seatRC[1])

        if row > 10 or col > 10:
            print("Lol...NO!")
            return False

        if check_if_seat_is_taken(row, col, seatMatrix, taken):
            print("Seat on row: {} col: {} is already taken!".format(row, col))
            return False

        seatMatrix.append((row, col))
    return seatMatrix

print(CANCEL_RESERVATION_PIC)
print(CONFIRM_RESERVATION_PIC)
