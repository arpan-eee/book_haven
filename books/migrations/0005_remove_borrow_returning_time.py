# Generated by Django 5.0 on 2024-01-14 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_borrow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='borrow',
            name='returning_time',
        ),
    ]
