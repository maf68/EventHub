from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django_countries.fields import CountryField
from datetime import timedelta
from django.db.models import Avg

CHOICES = (
      ('General', 'General'),('Music_Festivals', 'Music Festivals'), ('Art_Exhibitions', 'Art Exhibitions'), ('Theatre_Performances', 'Theatre Performances'), ('Dance_Shows', 'Dance Shows'), ('Film_Festivals', 'Film Festivals'), ('Marathons', 'Marathons'), ('Triathlons', 'Triathlons'), ('Football_Matches', 'Football Matches'), ('Basketball_Games', 'Basketball Games'), ('Olympic_Games', 'Olympic Games'), ('Debates', 'Debates'), ('Fundraisers', 'Fundraisers'), ('Fairs', 'Fairs'), ('Parades', 'Parades'), ('Farmers_Markets', 'Farmers Markets'), ('Charity_Events', 'Charity Events'), ('Volunteer_Events', 'Volunteer Events'), ('Fashion_Shows', 'Fashion Shows'), ('Trade_Shows', 'Trade Shows'), ('Product_Launches', 'Product Launches'), ('Runway_Shows', 'Runway Shows')
    )
class Event(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    city = models.CharField(max_length=30)
    location = models.CharField(max_length=100)
    date = models.DateField(null=False, default= timezone.now, validators=[MinValueValidator(timezone.now().date())])
    promoter = models.ForeignKey('MyUser', on_delete=models.CASCADE, related_name='events')
    attendees = models.ManyToManyField('MyUser', related_name='events_attending', blank = True)
    following = models.ManyToManyField('MyUser', related_name='events_following', blank = True)
    poster = models.URLField(blank = True)
    duration = models.DurationField(default=timedelta(hours=1))
    event_type = models.CharField(max_length=255, choices = CHOICES, default='General')
    avg_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=0)
    request_choices = (
        ("Accept", "Accept"),
        ("Reject", "Reject"),
        ("Pending", "Pending"),
    )
    request_status = models.CharField(
        max_length=20,
        choices=request_choices,
        default="Pending",
    )
    #image_urls = models.TextField(blank=True) #If the image list if used, uncomment this and the functions for it below.
    def _str_(self):
        return self.title
    """
    def get_image_urls(self):
        return self.image_urls.split(',')

    def add_image_url(self, url):
        if self.image_urls:
            self.image_urls += ',{}'.format(url)
        else:
            self.image_urls = url
        self.save()    
    """
    def get_average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            total_ratings = sum([review.rating for review in reviews])
            return round(total_ratings / len(reviews), 1)
        else:
            return 0
    def get_num_ratings(self):
        return self.reviews.count()
    def save(self, *args, **kwargs):
        self.avg_rating = self.get_average_rating()
        super(Event, self).save(*args, **kwargs)

class MyUser(AbstractUser):
    date_of_birth = models.DateField(blank=True, null=True)
    nationality = CountryField(blank = True)
    address = models.CharField(blank = True, max_length=300)
    is_promoter = models.BooleanField(default=False)
    bio = models.CharField(max_length=500, default="", blank=True)
    picture = models.URLField(blank = True, null=True)
    preferance_type = models.CharField(max_length=255, choices = CHOICES, default='General')
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

class Review(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='reviews')
    comment = models.CharField(max_length=500)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.event.title} by {self.user.username}'
    def delete(self, using=None, keep_parents=False):
        event = self.event
        super().delete(using=using, keep_parents=keep_parents)
        event.save()

class Announcement(models.Model):
    title = models.CharField(max_length = 150, blank = False, default = "")
    description = models.CharField(max_length = 600, blank = False)
    image = models.URLField(blank=True, null= True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='announcement_event', blank=False)
    def _str_(self):
        return f'Announcement for {self.event.title} titled {self.title}'
    
