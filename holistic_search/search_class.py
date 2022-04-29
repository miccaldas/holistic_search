"""
Class that will search the notes and bookmarks databases for a
common query. It'll aggregate the results and present them.
"""
import click
import isort
import snoop
from mysql.connector import Error, connect
from snoop import pp


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


class Search:
    """
    We'll make fulltext searches for the query in both
    databases, and present the results.
    """

    def __init__(self, query):
        self.query = query

    def bkmks_search(self):
        """
        Searches the bookmarks database for the query.
        """
        try:
            conn = connect(host="localhost", user="mic", password="xxxx", database="bkmks")
            cur = conn.cursor()
            query = f"SELECT title, comment, link FROM bkmks WHERE MATCH(title, comment, link, k1, k2, k3) AGAINST ('{self.query}')"
            cur.execute(query)
            bkmks_records = cur.fetchall()
            conn.close()
        except Error as e:
            print("Error while connecting to db", e)
        return bkmks_records

    def notes_search(self):
        """
        Searches the notes database for the query.
        """
        try:
            conn = connect(host="localhost", user="mic", password="xxxx", database="notes")
            cur = conn.cursor()
            query = f"SELECT title, note FROM notes WHERE MATCH(title, k1, k2, k3, note, url) AGAINST ('{self.query}')"
            cur.execute(query)
            notes_records = cur.fetchall()
            conn.close()
        except Error as e:
            print("Error while connecting to db", e)
        return notes_records

    def presentation(self):
        """
        Defines the presentation of the data to the user.
        """
        bkmks = self.bkmks_search()
        notes = self.notes_search()

        print(click.style(" -------------------- BOOKMARKS ----------------", fg="bright_green", bold=True))
        print("\n")
        for i in bkmks:
            print(click.style(f" [»»] - {i[0]}", fg="bright_red", bold=True))
            print(click.style(f" {i[1]}", fg="bright_white", bold=True))
            print(click.style(f" {i[2]}", fg="bright_white", bold=True))
            print("\n")
        print(click.style(" -------------------- NOTES --------------------", fg="bright_green", bold=True))
        print("\n")
        for row in notes:
            print(click.style(f" [&&] - {row[0]}", fg="bright_red", bold=True))
            print(click.style(f" {row[1]}", fg="bright_white", bold=True))
            print("\n")
