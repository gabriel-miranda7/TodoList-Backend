# Generated by Django 5.0.4 on 2024-04-21 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_todo_favorite_alter_todo_isontrashbin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='favorite',
        ),
        migrations.AddField(
            model_name='todolist',
            name='favorite',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
