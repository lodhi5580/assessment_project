# Generated by Django 5.1.6 on 2025-02-27 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crud_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='prise',
            new_name='price',
        ),
    ]
