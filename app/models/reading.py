from django.db import models

from .book import Book
from django.contrib.auth.models import User


class Reading(models.Model):
    """Reading model."""
    score = models.FloatField("Score")
    comment = models.TextField("Comment")

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.book.title
