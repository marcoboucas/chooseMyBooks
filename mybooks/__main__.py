"""Recommender System for books."""
import os

from dotenv import load_dotenv

from src.library.library import Library


load_dotenv()

library = Library(
    api_key=os.getenv("apiKey", "")
)
