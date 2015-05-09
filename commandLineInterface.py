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

    reservationData(projectionChoice, booked_seats)

    cursor.close()
    connection.close()


def reservationData(projection_id, booked_seats):
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
        print("THANK YOU!")
    else:
        print("""                               :oooooooooo:
                        ::oOOOOooo:::::ooooO88Oo:
                  :O8O:                           oO8o
              o8o                                      :8o
             88:                                         O8:
          8O:                                               oO
         8o                                                  oO
        8o                                                    Oo
      :8o                                              :      :8:
     :8:                                               :       :8:
    O::o                                              oo         8:
   :o:ooO                                             oo         o8
   8    oo                                            :o          8o
  8      o8:                                            O8O:       8:
 o:     ::88:                                             O8        8
 8       888:                                             O8o       O
:8       :88:                                             888Ooo:   oo
Oo       O88           :oO88O:            oO88Oo:         O8888O    :O
O:  ::   :88      :oO888888888:          8888888888OOo:    8888:    :O
O:  :o    8o   o88888888888888:          88888888888888O:   o88     :O
Oo   oo  oO  o888888888888888O           8888888888888888o   88     :O
:O    O: oo  8888888888888888:          o88888888888888888   88     :O
 O:   :88:   O88888888888888888           O888888888888888  o88888888O
  o   :8O    o888888888888888O            O88888888888888O   88888888o
  O:  :8:    88888888888888O:      :      O888888888888888   O8888888:
  :O  :8     88888888888888       o88:    :o88888888888888    8888888
   OoooO    :8888888888O:8o      :8O88       :O8888888888o     O888oo
    888:     8888888o:  8O       :8o88O         O888888O:          :
    :88       oOOo:   :O:        :8:888          8o               :
     88              o:          88oO88o      :: :oo            :
     88::               oo      O88O:888o    O8o:   :   ::     : :
     8o o:                     o88oo O888    :8        :88   :: ::
     oO  oo     o              O8o : O888     :o       oO8o ::  O
      O:  Oo  ::o              OO    OO :             :oO88 O::O:
       O  :8: :88o             OO    Oo             :O888O  8OO:
       oo  Oo  O888o           :O:o:  :            o8888o  :O
        :O888  :88888           :o  Oo            o8888o   8:
           :8:  O8888               8            :O888O   :8
            Oo  :8888               o             :888    :O
            :O   o888  ::                         o88:    Oo
            :O    O88OO8oOOoOOoOooOooOOOOOOOOOO88O88O     O:
            OO     888:: o :o: o  o   O: 8: O o::o 8:     8
           :8O     :88o:  :    :  :      ::        8      O
           O8o      Oo:8oo:    :          :   :::oo8     :O
           88o      Oo :      o:o: :o    Oo : :  o       :O
           88O       :oo:oo:o o :  :: oo :: o O::o       o:
           888         :::::oO8O8OoO8O88oOOoo:         :Oo
            O88Oo::               ::                  :O
             :oO8888o                               :Oo
                 :o88o                      oo    o8O:
                     o8O     Oo    o           o88
                     :88o        O:          O88
                        O88o     :8o        o88O
                          o88ooOO888O::::oO88O:
                            o8888888888888Oo """)


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


make_reservation()
