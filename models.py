from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

class Event(models.Model): 
    title = models.CharField(max_length=80)
    description = models.TextField(max_length=2000)                                            
    city = models.CharField(max_length=30)
    location = models.CharField(max_length=100)
    promoter = models.ForeignKey('MyUser', on_delete=models.CASCADE, related_name='events')
    attendees = models.ManyToManyField('MyUser', related_name='events_attending', default="") 
    following = models.ManyToManyField('MyUser', related_name='events_following', default="")
    def __str__(self):
        return self.title
    

class MyUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=56)
    address = models.CharField(max_length=300)
    #is_promoter = models.BooleanField(default=False)
    is_promoter_choices = (('A','Attendee'),('P','Promoter'),)
    is_promoter = models.CharField(max_length=1, choices=is_promoter_choices)
    #bio = models.CharField(max_length=500, default="")
    #picture = models.URLField(blank = True)
    username = models.CharField(max_length=30, primary_key=True)
    password1 = models.CharField(max_length=30, default="")
    password2 = models.CharField(max_length=30, default="")
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
