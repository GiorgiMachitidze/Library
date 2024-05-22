from django.contrib import admin
from .models import *


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'publication_date', 'stock_quantity']
    list_filter = ['genres', 'publication_date']
    search_fields = ['title', 'authors__name', 'genres__name']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']


admin.site.register(Client)
admin.site.register(Employer)
