# This is a sample Python script.
import psycopg2
from datetime import datetime, timezone
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def empty_table():
    conn = psycopg2.connect("dbname=postgres user=j3_g2 password=Blaat1234 host=145.74.104.145")    #connectie maken aan database
    cur = conn.cursor()

    date = '2000-09-09'     #moduleren zodat we later dingen in de querry konden zetten


    cur.execute('SELECT * from condition_occurrence;')
    db_version = cur.fetchone()
    # print("condition_occurrrence")
    # print(db_version)

    cur.execute('delete from condition_occurrence;')
    cur.execute('SELECT * from condition_occurrence;')
    db_version = cur.fetchone()
    # print(db_version)

    cur.execute('SELECT * from person;')
    db_version = cur.fetchone()
    # print("person")
    # print(db_version)

    cur.execute('delete from person;')
    cur.execute('SELECT * from person;')
    db_version = cur.fetchone()
    # print(db_version)

    cur.execute('SELECT * from measurement;')
    db_version = cur.fetchone()
    # print("measurement")
    # print(db_version)

    cur.execute('delete from measurement;')
    cur.execute('SELECT * from measurement;')
    db_version = cur.fetchone()
    # print(db_version)

    conn.commit()
    cur.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    empty_table()
