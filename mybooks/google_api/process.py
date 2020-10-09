"""Process the data from google api to the right format."""
from typing import Any, Dict


def process_book(book: Dict[str, Any]):
    """Process one book."""
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
        "author": volume_info.get("authors", [""])[0],
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


if __name__ == "__main__":
    import os
    import json
    from pprint import pprint
    from dotenv import load_dotenv

    load_dotenv()
    file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../data/book_example.json"
    )
    with open(file, "r") as _:
        data = json.load(_)
    pprint(process_book(data))
