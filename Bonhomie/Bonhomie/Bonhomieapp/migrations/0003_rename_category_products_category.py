# Generated by Django 5.0 on 2023-12-20 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bonhomieapp', '0002_rename_category_category_title_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='Category',
            new_name='category',
        ),
    ]
