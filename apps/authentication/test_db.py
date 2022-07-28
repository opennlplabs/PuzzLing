import sqlite3 as db

db_path = "../db.sqlite3"
exectCmd = "SELECT rowid, * FROM Users;"


# print all the rows from the database
def readFronSqllite(db_path, exectCmd):
    """

    :param db_path:
    :param exectCmd:
    :return:
    """
    conn = db.connect(db_path)
    cursor = conn.cursor()
    conn.row_factory = db.Row
    cursor.execute(exectCmd)
    rows = cursor.fetchall()
    return rows
