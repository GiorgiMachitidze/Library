# Generated by Django 4.2 on 2024-05-22 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0008_employer_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='fullname',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='personal_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
