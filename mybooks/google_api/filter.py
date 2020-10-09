"""Filter books."""


def filter_book(book) -> bool:
    """Filter a book."""
    # Check Language
    if book['language'] != "fr":
        return False

    # Check if author (else probably an "Integrale")
    if book["authors"] is None:
        return False

    if len(book['ISBN13']) == 0 and len(book['ISBN10']) == 0:
        return False
    return True
