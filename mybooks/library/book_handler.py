"""Data Handler for library."""

from typing import List, Dict, Tuple
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
        report = {}
        for book in data:
            transformed_book = transform_book(book)
            test_filter, report = self.filter_book(transformed_book, report)
            if test_filter:
                add_to_library.append(transformed_book)

        # Display information on a update
        print(f"Fetched {len(data)} books")
        print(f"Added {len(add_to_library)} in the library")
        for key, value in report.items():
            print(f"Filter {key} expelled {value} books")
        print('\n' * 2)

        # Add to the library
        self.library = pd.concat([
            self.library,
            pd.DataFrame.from_dict(add_to_library)
        ])
        self.compute_values()

    def filter_book(self, book, report: Dict[str, int]) -> Tuple[bool, Dict[str, int]]:
        """Filter a book."""
        # check if book not already in the library
        try:
            if book['id'] in self.ids:
                return False, increment_dict(report, "already_in_library")
        except:
            pass

        # Check Language
        if book['language'] != "fr":
            return False, increment_dict(report, "language_not_fr")

        # Check if author (else probably an "Integrale")
        if book["authors"] is None:
            return False, increment_dict(report, "author_not_found")

        if len(book['ISBN13']) == 0 and len(book['ISBN10']) == 0:
            return False, increment_dict(report, "not_identifiants")
        return True, report

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

    # Search the link of the element
    link = "".join([
        f"{link[0]}?",
        *list(
            filter(
                lambda x: x.startswith('id='),
                link[1].split('&')
            )
        )
    ])

    # Search the identifiers
    try:
        identifiers = dict(list(
            map(lambda x: (x["type"], x['identifier']), volume_info["industryIdentifiers"])
        ))
    except KeyError:
        identifiers = {}

    # Select all the information available
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


def increment_dict(report: Dict[str, int], key: str) -> Dict[str, int]:
    """Increment the value by one."""
    try:
        report[key] += 1
    except KeyError:
        report[key] = 1
    return report
