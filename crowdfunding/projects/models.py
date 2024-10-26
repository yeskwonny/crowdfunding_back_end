from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta,date
from django.db.models import Sum
# from django.utils import timezone

class Project(models.Model):
    title = models.CharField(max_length=200)
    director=models.CharField(max_length=200)
    movie_synopsis = models.TextField()
    genres=models.CharField(max_length=100)
    goal = models.IntegerField()
    goal_deadline= models.DateTimeField()
    # goal_deadline= models.DateTimeField(default=datetime.now())
    image = models.URLField()
    is_open = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )
    # sum pledge
   
    @property
    def pledge_total(self):
        total = self.pledges.aggregate(amount_sum=Sum('amount'))['amount_sum']
        return total or 0 
    
    @property
    def is_goal_reached(self):
        return self.pledge_total >= self.goal
       


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