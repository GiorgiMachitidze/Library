from datetime import timezone, datetime, timedelta

from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Genre Name")

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        ordering = ['name']

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="Author Name")
    biography = models.TextField(verbose_name="Biography")
    born_date = models.DateField(verbose_name="Born Date")

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    authors = models.ManyToManyField(Author, verbose_name="Authors")
    genres = models.ManyToManyField(Genre, verbose_name="Genres")
    title = models.CharField(max_length=200, verbose_name="Title")
    publication_date = models.DateField(verbose_name="Publication Date")
    stock_quantity = models.IntegerField(verbose_name="Stock Quantity")
    reserved_quantity = models.IntegerField(verbose_name="Reserved", default=0)
    all_reserved_quantity = models.IntegerField(verbose_name="Reserved all the time", default=0)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['title']

    def __str__(self):
        return self.title


class Reservation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    reserved_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.expiry_date:
            self.expiry_date = datetime.now() + \
                               timedelta(hours=20)
        super().save(*args, **kwargs)


class BookIssue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    def is_returned(self):
        return self.returned_at is not None