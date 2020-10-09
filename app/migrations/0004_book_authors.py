# Generated by Django 3.1.2 on 2020-10-04 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_author_reading'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(related_name='Authors', to='app.Author'),
        ),
    ]