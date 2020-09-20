"""Fill the library with some books."""


import os

from dotenv import load_dotenv

from .library import Library


load_dotenv()


TO_SEARCH = [
    "rowling",
    "pierre bottero",
    "Robin Hobb",
    "Maxime Chattam",
    "Valérie Perrin",
    "Franck Thilliez",
    "Amélie Jeannot",
    "Stephenie Meyer",
    "Tolkien",
    "Brandon Sanderson",
    "Robert Jordan",
    "Terry Pratchett",
    "Lovecraft",
    "Stephen King",
    "Patrick Rothfuss",
    "Neil Gaiman",
    "Lewis",
    "Terry Brooks",
    "Ray Bradbury",
    "Roald Dahl",
    "George Martin",
    "David Eddings",
    "Lewis Carrol",
    "Steven Erikson",
    "Rick Riordan",
    "Andrzej Sapkowski",
    "Terry Goodkind",
    "Isaac Asimov",
    "Christopher Paolini",
    "David Gemmell",
    "Anthony Horowitz",
    "Sarah Maas"
]

if __name__ == "__main__":
    library = Library(api_key=os.getenv('apiKey', ""))
    for search in TO_SEARCH:
        print(f"Search for {search}")
        library.fetch_and_save(author=search)
    print(library.library[['title']].head(80))
