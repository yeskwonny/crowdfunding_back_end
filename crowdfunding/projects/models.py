from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta,date
from django.db.models import Sum


class Project(models.Model):
    title = models.CharField(max_length=200)
    director=models.CharField(max_length=200)
    movie_synopsis = models.TextField()
    genres=models.CharField(max_length=100)
    goal = models.IntegerField()
    goal_deadline= models.DateTimeField(default=date.today)
    image = models.URLField()
    is_open = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )
    # sum pledge
    def pledge_total(self):
        total = self.pledges.aggregate(Sum('amount'))
        return total or 0  # If no pledges, return 0


class Pledge(models.Model):
    amount=models.IntegerField()
    comment=models.CharField(max_length=200)
    anonymous=models.BooleanField()
    project=models.ForeignKey('Project',on_delete=models.CASCADE,related_name='pledges')
    supporter=models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='pledges'
    )