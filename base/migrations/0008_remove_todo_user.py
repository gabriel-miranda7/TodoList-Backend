# Generated by Django 5.0.4 on 2024-04-21 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_todo_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='user',
        ),
    ]
