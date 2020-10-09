from django.contrib import admin


from .models.book import Book
from .models.author import Author
from .models.reading import Reading


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', "authors_names", "isbn13")

    def authors_names(self, obj):
        return " ".join([x.name for x in obj.authors.all()])


class ReadingAdmin(admin.ModelAdmin):
    list_display = ('book', )


admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Reading, ReadingAdmin)
