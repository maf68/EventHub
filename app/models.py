from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator
#from django.contrib.postgres.fields import ArrayField

class MyUser(AbstractUser):
    date_of_birth = models.DateField(blank=True, null = True)
    nationality = models.CharField(max_length=56)
    address = models.CharField(max_length=300)
    is_promoter = models.BooleanField(default=False)
    bio = models.CharField(max_length=500, default="")
    picture = models.URLField(blank = True)
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

class Event(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField(max_length=2000, default="")
    city = models.CharField(max_length=30, default = "")
    location = models.CharField(max_length=100, default = "")
    date = models.DateField(null=False, default= timezone.now, validators=[MinValueValidator(timezone.now().date())])
    promoter = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='events', blank=True, null = True)
    #attendees = models.ManyToManyField(MyUser, related_name='events_attending')
    following = models.ManyToManyField(MyUser, related_name='events_following')
    #image_urls = models.TextField(blank=True)
    poster = models.URLField(blank=True)
    def __str__(self):
        return self.title
    #def get_image_urls(self):
    #    return self.image_urls.split(',')

    #def add_image_url(self, url):
    #    if self.image_urls:
    #        self.image_urls += ',{}'.format(url)
    #    else:
    #        self.image_urls = url
    #    self.save()    

class Announcement(models.Model):
    title = models.CharField(max_length = 150, blank = False, default = "")
    description = models.CharField(max_length = 600, blank = False)
    image = models.URLField(blank=True, null= True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='announcement_event', blank=False)