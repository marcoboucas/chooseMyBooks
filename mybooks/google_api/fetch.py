"""Fetch Google Books API."""
from typing import List, Any
from time import sleep
from random import randint
import requests
import os


def fetch_api(
        tag: str,
        author: str):
    """Fetch the google books api with an author name."""
    # Transform tags and authors into request get params
    tags = tag.lower().split(' ')
    authors = list(map(lambda x: "inauthor:" + x, author.lower().split(' ')))
    params = "+".join(tags + authors)

    # Loop over all books of the author by batch of size 40
    result_len = 40
    final_result: List[Any] = []
    last_id = 0
    while result_len == 40:
        # Make a time pause between calls
        sleep(randint(1, 3))

        result = requests.get(
            f'https://www.googleapis.com/books/v1/volumes?q={params}',
            params={
                "key": os.getenv('API_KEY'),
                "langRestrict": "fr",
                "maxResults": "40",
                "startIndex": str(last_id)
            }
        )
        result_json = result.json()

        # Check if there are some books
        try:
            result_json = result_json['items']
        except:
            print("No results for this")
            return final_result

        result_len = len(result_json)
        last_id += 40

        final_result.extend(result_json)

    return final_result


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    print(fetch_api(tag="Harry potter reliques", author="Rowling"))
