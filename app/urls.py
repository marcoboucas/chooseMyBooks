# Urls
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('map', views.map, name='map'),
    path('mapEdit', views.map_edit, name='map'),
    path('api/getBooks', views.get_books, name='get_books'),
    path('exportDatabase', views.export_database, name="Export Database")
]
