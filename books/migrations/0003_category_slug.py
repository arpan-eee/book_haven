# Generated by Django 5.0 on 2024-01-14 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_book_author_alter_book_image_alter_comment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]