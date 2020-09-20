"""API Requests for the Library."""

from typing import List, Any
from time import sleep
from random import randint

import requests

from .loader import LibraryLoader


class APICaller(LibraryLoader):
    """API Handler."""

    api_key: str

    def fetch_api(
        self,
        tag: str = "",
        author: str = ""
    ) -> List[Any]:
        """Fetch data from the API."""
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
                    "key": self.api_key,
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

    def fetch(self, *args, **kwargs):
        """Save the result of an API."""
        data = self.fetch_api(* args, **kwargs)

        if len(data) == 0:
            print("No result for this")
            print(args, kwargs)
        else:
            # Update the library
            self.update_library(data)
