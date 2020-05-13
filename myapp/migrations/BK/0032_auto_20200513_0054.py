# Generated by Django 2.2.12 on 2020-05-12 15:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0031_remove_okini_program'),
    ]

    operations = [
        migrations.AddField(
            model_name='okini',
            name='program',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='okini_program', to='myapp.Program'),
        ),
        migrations.AddField(
            model_name='okini',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='okini_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
