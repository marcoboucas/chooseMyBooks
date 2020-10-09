from django.db import models


class Author(models.Model):
    """Author model."""
    name = models.CharField("Name", max_length=100)

    def __str__(self):
        return self.name
