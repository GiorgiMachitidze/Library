# Generated by Django 4.2 on 2024-05-26 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0024_bookissue_have_to_return_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookissue',
            name='is_taken',
            field=models.BooleanField(default=False, verbose_name='Is taken?'),
        ),
        migrations.AlterField(
            model_name='bookissue',
            name='have_to_return_at',
            field=models.DateTimeField(null=True, verbose_name='Date of return'),
        ),
        migrations.AlterField(
            model_name='bookissue',
            name='issued_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Issue Date'),
        ),
        migrations.AlterField(
            model_name='bookissue',
            name='returned_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Returned at'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='expiry_date',
            field=models.DateTimeField(null=True, verbose_name='Date of expiration'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reserved_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Reservation date'),
        ),
    ]
