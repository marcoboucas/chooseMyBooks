# Generated by Django 3.1.2 on 2020-10-08 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20201004_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='google_id',
            field=models.CharField(default='', max_length=100, unique=True, verbose_name='Google ID'),
        ),
    ]