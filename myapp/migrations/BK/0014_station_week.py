# Generated by Django 2.2.12 on 2020-05-09 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_auto_20200510_0124'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='week',
            field=models.IntegerField(blank=True, choices=[(1, '月'), (2, '火'), (3, '水'), (4, '木'), (5, '金'), (6, '土'), (7, '日')], null=True, verbose_name='曜日'),
        ),
    ]
