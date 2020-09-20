"""Data Handler for library."""

from typing import List
import pandas as pd


class BookHandler():
    """Book Handler."""

    library: pd.DataFrame
    nbr_books: int
    ids: List[str]

    def update_library(self, data):
        """Update the library."""
        # Add new elements in the library
        add_to_library = []
        for book in data:
            transformed_book = transform_book(book)
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

    def compute_values(self):
        """Compute informations about the library."""
        self.nbr_books = self.library.shape[0]
        try:
            self.ids = self.library['id'].astype(str).tolist()
        except:
            self.ids = []

        # Change the types of the library
        for col in ["id", "title", "ISBN13", "ISBN10", "thumbnail", "language", "link"]:
            self.library[col] = self.library[col].astype(str)

        for col in ['ISBN13', "ISBN10"]:
            self.library[col] = self.library[col].astype(str).apply(lambda x: x.split('.')[0])

        for col in ['authors', "categories"]:
            try:
                self.library[col] = self.library[col].apply(
                    lambda x: list(map(lambda _: _[1:-1], x.strip('][').split(',')))
                )
            except:
                pass
        for col in ['pageCount']:
            self.library[col] = self.library[col].astype(int)


def transform_book(book):
    """Select only the needed data."""
    volume_info = book['volumeInfo']
    link = volume_info['previewLink'].split('?')
    link = "".join(
        [link[0] + "?"] + list(filter(lambda x: x.startswith('id='), link[1].split('&'))))
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
