"""Module that will call the script functions."""
import click
import isort
import snoop
from snoop import pp

from search_class import Search


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


@snoop
def main():
    """
    We'll ask the user for a query term and feed it to 'Search class'.
    """

    ask = input(click.style("[&&] - What is your query? ", fg="bright_red", bold=True))

    search = Search(ask)
    search.presentation()


if __name__ == "__main__":
    main()
