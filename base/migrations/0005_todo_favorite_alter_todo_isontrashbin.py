# Generated by Django 5.0.4 on 2024-04-21 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_todo_options_todo_isontrashbin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='favorite',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='todo',
            name='isOnTrashBin',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
