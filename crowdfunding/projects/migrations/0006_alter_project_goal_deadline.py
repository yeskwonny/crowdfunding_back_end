# Generated by Django 5.1 on 2024-10-19 00:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_alter_project_goal_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='goal_deadline',
            field=models.DateTimeField(default=datetime.date.today),
        ),
    ]
