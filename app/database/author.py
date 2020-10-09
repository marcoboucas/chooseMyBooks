"""Handle the author."""
from ..models import Author


def get_all_authors():
    """Get all authors."""
    return Author.objects.all()


def get_author(name: str):
    """Get one author by name."""
    return Author.objects.get(name)
