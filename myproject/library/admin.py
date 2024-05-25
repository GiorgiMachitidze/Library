from django.contrib import admin
from .models import *

@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ('book', 'client', 'issued_at', 'returned_at', 'is_returned')

class BookIssueInline(admin.TabularInline):
    model = BookIssue
    readonly_fields = ('issued_at', 'returned_at')
    can_delete = False

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'publication_date', 'stock_quantity']
    list_filter = ['genres', 'publication_date']
    search_fields = ['title', 'authors__name', 'genres__name']
    inlines = [BookIssueInline]
    def issued_count(self, obj):
        return obj.issued_count()

    issued_count.short_description = 'Times Issued'


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
admin.site.register(Reservation)

