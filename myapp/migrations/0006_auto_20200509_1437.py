# Generated by Django 2.2.12 on 2020-05-09 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_station'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post',
            new_name='program',
        ),
    ]