# Generated by Django 4.2 on 2024-05-25 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0017_book_all_reserved_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='is_reserved',
        ),
    ]