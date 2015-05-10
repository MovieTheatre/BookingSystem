import sqlite3
from settings import VAR_DB_NAME, TABLES, CONFIRM_RESERVATION_PIC, CANCEL_RESERVATION_PIC
from cinema_interface import CliInterface
from cinema_db import CinemaDatabaseManager


def main():
    conn = sqlite3.connect(VAR_DB_NAME)
    conn.row_factory = sqlite3.Row

    cinema_manager = CinemaDatabaseManager(conn)
    interface = CliInterface(cinema_manager)

    interface.start()


if __name__ == "__main__":
    main()
