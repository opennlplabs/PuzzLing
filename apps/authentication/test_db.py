import sqlite3 as db


# exectCmd = "SELECT rowid, * FROM Users;"

# print all the rows from the database
def readFromSqlite(exectCmd):
    """
    :param db_path:
    :param exectCmd:
    :return:
    """
    db_path = "../db.sqlite3"
    conn = db.connect(db_path)
    cursor = conn.cursor()
    conn.row_factory = db.Row
    cursor.execute(exectCmd)
    rows = cursor.fetchall()
    return rows