from django.db import models

from .author import Author

LANG_CHOICES = [
    ("fr", "French"),
    ('en', "English")
]


class Book(models.Model):
    """Book model."""
    google_id = models.CharField("Google ID", max_length=100, unique=True)
    title = models.CharField("Title", max_length=100)
    lang = models.CharField("Lang", choices=LANG_CHOICES, default="fr", max_length=2)

    isbn13 = models.CharField("ISBN13", max_length=14, default="x" * 13)
    isbn10 = models.CharField("ISBN10", max_length=11, default="x" * 10)

    link = models.CharField("Link", max_length=500, null=True)
    thumbnail = models.CharField("Thumbnail", max_length=500, null=True)

    x = models.FloatField("X", default=0.0)
    y = models.FloatField("Y", default=0.0)

    description = models.TextField("Description")

    authors = models.ManyToManyField(Author, "Authors")

    def __str__(self):
        return self.title
