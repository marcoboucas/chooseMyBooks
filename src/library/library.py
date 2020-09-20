"""
Library class for books.
"""

import os

from .api_caller import APICaller


class Library(APICaller):
    """Library Object."""

    def __init__(
        self,
        api_key: str,
        file: str = "./library.csv"
    ):
        """Init."""
        self.api_key = api_key
        self.file = file
        self.load_library()


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    library = Library(api_key=os.getenv('apiKey', ""))
    library.fetch_and_save(tag="", author="Bernard Minier")
    # library.fetch_and_save(author="pierre bottero")
    print(library.library[['title', 'ISBN13']].head(80))
