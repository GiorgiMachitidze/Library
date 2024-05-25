# Generated by Django 4.2 on 2024-05-25 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0018_remove_book_is_reserved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='book',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='client',
        ),
        migrations.AddField(
            model_name='reservation',
            name='book',
            field=models.ManyToManyField(to='library.book', verbose_name='Book'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='client',
            field=models.ManyToManyField(to='library.client', verbose_name='Client'),
        ),
    ]