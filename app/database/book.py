"""Handle the books database."""
import django
import logging

from ..models import Book, Author


def get_all_books():
    """Get all books."""
    return Book.objects.all()


def add_book(book):
    """Add a book to the library."""
    # Check if book not already in the library
    try:
        new_book = Book(
            google_id=book['id'],
            title=book['title'],
            lang=book['language'],
            isbn10=book['ISBN10'],
            isbn13=book['ISBN13'],
            link=book['link'],
            thumbnail=book['thumbnail'],
            description=book['description'],
        )
        new_book.save()

        # Add the authors
        authors = []
        for author in book['authors']:
            author, _ = Author.objects.get_or_create(name=author)
            authors.append(author.id)
        new_book.authors.set(authors)
        new_book.save()

    except django.db.utils.IntegrityError:
        logging.warning("This book is already present in the database %s (%s)", book['title'], book['id'])
    return True
