"""
Library class for books.
"""

import os
import json

import requests
import pandas as pd


class Library:
    """Library Object."""

    def __init__(
        self,
        api_key: str,
        folder: str = ".",
        filename: str = "library"
    ):
        """Init."""
        self.api_key = api_key
        self.folder = folder
        self.file_path = os.path.join(folder, filename+".csv")
        self.load_library()

    def fetch(self, tag: str = "", author: str = ""):
        """Fetch data from the API."""
        tags = tag.lower().split(' ')
        author = list(map(lambda x: "inauthor:"+x, author.lower().split(' ')))
        params = "+".join(tags + author)
        result = requests.get(
            f'https://www.googleapis.com/books/v1/volumes?q={params}',
            params={
                "key": self.api_key,
            }
        )
        return result.json()

    def fetch_and_save(self, *args, **kwargs):
        """Save the result of an API."""
        data = self.fetch(*args, **kwargs)

        # Save the request content
        with open(os.path.join(self.folder, "request.json"), "w") as file:
            file.write(json.dumps(data, ensure_ascii=True, indent=4))

        if len(data["items"]) == 0:
            print(args, kwargs)
            raise "Not found for that"

        if "items" in data:
            # Update the library
            self.update_library(data['items'])

            # Save library
            self.save_library()

    def update_library(self, data):
        """Update the library."""
        # Add new elements in the library
        add_to_library = []
        for book in data:
            transformed_book = self.transform_book(book)
            if self.filter_book(transformed_book):
                add_to_library.append(transformed_book)
        self.library = pd.concat([
            self.library,
            pd.DataFrame.from_dict(add_to_library)
        ])
        self.compute_values()

    def filter_book(self, book):
        """Filter a book."""
        # check if book not already in the library
        try:
            if book['id'] in self.ids:

                return False
        except:
            pass

        # Check Language
        if book['language'] != "fr":
            return False

        # Check if author (else probably an "Integrale")
        if book["authors"] is None:
            return False

        return True

    def transform_book(self, book):
        """Select only the needed data."""
        volume_info = book['volumeInfo']
        link = volume_info['previewLink'].split('?')
        link = "".join(
            [link[0]+"?"] + list(filter(lambda x: x.startswith('id='), link[1].split('&'))))
        identifiers = dict(list(
            map(lambda x: (x["type"], x['identifier']), volume_info["industryIdentifiers"])))

        transformed_book = {
            "id": book['id'],
            "title": volume_info['title'],
            "authors": volume_info.get("authors", None),
            "description": volume_info.get('description', ""),
            "ISBN13": str(identifiers.get('ISBN_13', "")),
            "ISBN10": str(identifiers.get('ISBN_10', "")),
            "categories": volume_info.get('categories', []),
            "pageCount": int(volume_info.get('pageCount', 0)),
            "thumbnail": volume_info.get('imageLinks', {"thumbnail": "none"})['thumbnail'],
            "language": volume_info['language'],
            "link": link
        }
        return transformed_book

    def load_library(self):
        """Load library."""
        try:
            self.library = pd.read_csv(self.file_path)
            self.library = self.library[~self.library['description'].isna()]
        except:
            self.library = pd.DataFrame()
        self.compute_values()

    def save_library(self):
        """Save library."""
        self.library.to_csv(self.file_path, index=False)

    def compute_values(self):
        """Compute informations about the library."""
        self.nbr_books = self.library.shape[0]
        try:
            self.ids = self.library['id'].astype(str).tolist()
        except:
            self.ids = []


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    library = Library(api_key=os.getenv('apiKey'))
    library.fetch_and_save(tag="", author="Bernard Minier")
    # library.fetch_and_save(author="pierre bottero")
    print(library.library[['title', 'ISBN13']].head(80))
