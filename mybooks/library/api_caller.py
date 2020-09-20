"""API Requests for the Library."""

import requests

from .loader import LibraryLoader


class APICaller(LibraryLoader):
    """API Handler."""

    api_key: str

    def fetch_api(self, tag: str = "", author: str = ""):
        """Fetch data from the API."""
        tags = tag.lower().split(' ')
        authors = list(map(lambda x: "inauthor:" + x, author.lower().split(' ')))
        params = "+".join(tags + authors)
        result = requests.get(
            f'https://www.googleapis.com/books/v1/volumes?q={params}',
            params={
                "key": self.api_key,
            }
        )
        return result.json()

    def fetch(self, *args, **kwargs):
        """Save the result of an API."""
        data = self.fetch_api(* args, **kwargs)

        if len(data["items"]) == 0:
            print(args, kwargs)
            raise "Not found for that"

        if "items" in data:
            # Update the library
            self.update_library(data['items'])
