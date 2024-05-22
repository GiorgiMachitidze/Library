import random
from django.core.management.base import BaseCommand
from faker import Faker
from library.models import *


class Command(BaseCommand):
    help = 'Populate the database with randomly generated books.'

    def handle(self, *args, **kwargs):
        faker = Faker()

        # Create some genres
        genres = []
        for _ in range(10):
            genre_name = faker.word()
            genre, created = Genre.objects.get_or_create(name=genre_name)
            genres.append(genre)

        # Create some authors
        authors = []
        for _ in range(50):
            author_name = faker.name()
            biography = faker.text(max_nb_chars=500)
            born_date = faker.date_of_birth(minimum_age=20, maximum_age=90)
            author, created = Author.objects.get_or_create(
                name=author_name,
                defaults={'biography': biography, 'born_date': born_date}
            )
            authors.append(author)

        # Create books
        for _ in range(1000):
            title = faker.sentence(nb_words=4)
            publication_date = faker.date_between(start_date='-30y', end_date='today')
            stock_quantity = faker.random_int(min=0, max=100)

            book = Book.objects.create(
                title=title,
                publication_date=publication_date,
                stock_quantity=stock_quantity,
            )

            # Add random authors to the book
            num_authors = random.randint(1, 5)
            book.authors.set(random.sample(authors, num_authors))

            # Add random genres to the book
            num_genres = random.randint(1, 3)
            book.genres.set(random.sample(genres, num_genres))

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with 1000 random books.'))
