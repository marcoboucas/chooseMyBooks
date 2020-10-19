from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
from django.core import serializers

import logging

import pandas as pd

from .database.book import get_all_books, add_book, vectorize_all_books
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

    context = {
        "message": "Welcome on this website !",
        "books": get_all_books(),
    }
    return render(request, 'index.html', context)


def map(request):
    context = {
        "message": "Welcome on the map !",
        "books": get_all_books()
    }
    return render(request, "map.html", context)


def map_edit(request):
    if request.method == "POST":
        print("Generate the vectors")
        vectorize_all_books()
    context = {
        "message": "Welcome on the map Edition !",
    }
    return render(request, "mapEdit.html", context)


def get_books(request):
    """API to get books."""
    data = serializers.serialize("json", get_all_books(), fields=('title', 'x', 'y'))
    return HttpResponse(data, content_type='application/json')


def export_database(request):
    """Export the database to a csv, to ease the data viz."""
    books = get_all_books()
    new_books = []
    for book in books:
        new_book = {}
        for attr in ['google_id', 'title', 'lang', 'isbn10', 'isbn13', 'link', 'thumbnail', 'x', 'y', 'description', 'authors']:
            new_book[attr] = getattr(book, attr)
        new_books.append(new_book)
    df = pd.DataFrame.from_records(new_books)
    df.to_csv('./exportDatabase.csv')
    return redirect('/')
