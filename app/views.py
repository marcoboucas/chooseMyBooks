from django.shortcuts import render
from django import forms

from .database.book import get_all_books, add_book
from mybooks.google_api import fetch_api, process_book, filter_book


class SearchForm(forms.Form):
    author = forms.CharField(label='author', max_length=100)


def index(request):
    # Search values
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            author = request.POST['author']
            if len(author) > 0:

                # Making the request
                raw_books = fetch_api(tag="", author=author)

                # Process the books
                processed_books = list(map(process_book, raw_books))

                # Filter the books
                filtered_books = list(filter(filter_book, processed_books))

                # Add books to library
                for book in filtered_books:
                    add_book(book)

    books = get_all_books()
    context = {
        "message": "Welcome on this website !",
        "books": books,
    }
    return render(request, 'index.html', context)
