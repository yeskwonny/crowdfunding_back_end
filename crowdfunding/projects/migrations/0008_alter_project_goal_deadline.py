# Generated by Django 4.2.5 on 2024-10-19 04:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_alter_project_goal_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='goal_deadline',
            field=models.DateTimeField(default=datetime.date.today),
        ),
    ]
