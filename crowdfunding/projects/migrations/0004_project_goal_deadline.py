# Generated by Django 5.1 on 2024-10-15 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_rename_description_project_movie_synopsis_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='goal_deadline',
            field=models.DateTimeField(default=1999),
            preserve_default=False,
        ),
    ]