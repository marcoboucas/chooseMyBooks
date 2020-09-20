"""Recommender System for books."""
import os

from src.server.app import create_app
from src.library.library import Library

from dotenv import load_dotenv
load_dotenv()

library = Library(
    api_key=os.getenv("apiKey")
)

app = create_app(library)
app.run(
    port=3000,
    debug=True
)