from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import viewsets


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

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['title']

    def __str__(self):
        return self.title
