# Generated by Django 5.0.4 on 2024-04-19 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_remove_todolist_todos_todo_todolist'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todo',
            options={'ordering': ['-complete']},
        ),
        migrations.AddField(
            model_name='todo',
            name='isOnTrashBin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='todo',
            name='timeOfTrashBin',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='todo',
            name='complete',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='todo',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
