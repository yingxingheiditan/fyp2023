from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

#model for profiles
class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete= models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    current_streak = models.IntegerField(default=0)
    highest_streak = models.IntegerField(default=0)
    profile_image = models.ImageField(upload_to='testApp/static/profileImage', default='testApp/static/profileImage/default.png', blank=True)
    following = models.ManyToManyField(User, blank=True, related_name='following')

#model to track dates
class Completed_Dates(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, verbose_name='user', related_name='completed_dates', on_delete= models.CASCADE)
    completed = models.BooleanField()
    date = models.DateField()
#note: this prototype is an offline version.
#      In real world implementation, we will need a running server to update the backend
#      data daily, to keep track of the days.

#model for day of exercise
class Exercise_Day(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='exercise_day', on_delete= models.CASCADE)
    mon = models.BooleanField(default=True)
    tue = models.BooleanField(default=True)
    wed = models.BooleanField(default=True)
    thu = models.BooleanField(default=True)
    fri = models.BooleanField(default=True)
    sat = models.BooleanField(default=True)
    sun = models.BooleanField(default=True)
