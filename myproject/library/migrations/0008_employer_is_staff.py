# Generated by Django 4.2 on 2024-05-22 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_remove_employer_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
