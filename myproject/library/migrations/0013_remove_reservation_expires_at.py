# Generated by Django 4.2 on 2024-05-25 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0012_book_is_reserved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='expires_at',
        ),
    ]