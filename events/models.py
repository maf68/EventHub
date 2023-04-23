from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import timedelta
from django.db.models import Avg


class Event(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    city = models.CharField(max_length=30)
    location = models.CharField(max_length=100)
    date = models.DateField(null=False, default= timezone.now, validators=[MinValueValidator(timezone.now().date())])
    promoter = models.ForeignKey('MyUser', on_delete=models.CASCADE, related_name='events')
    attendees = models.ManyToManyField('MyUser', related_name='events_attending')
    following = models.ManyToManyField('MyUser', related_name='events_following')
    poster = models.URLField(blank = True)
    duration = models.DurationField(default=timedelta(hours=1))
    event_type = models.CharField(max_length=255, default='General')

    def _str_(self):
        return self.title

    def get_image_urls(self):
        return self.image_urls.split(',')

    def add_image_url(self, url):
        if self.image_urls:
            self.image_urls += ',{}'.format(url)
        else:
            self.image_urls = url
        self.save()    
    def get_average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            total_ratings = sum([review.rating for review in reviews])
            return round(total_ratings / len(reviews), 1)
        else:
            return 0

class MyUser(AbstractUser):
    date_of_birth = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=56)
    address = models.CharField(max_length=300)
    is_promoter = models.BooleanField(default=False)
    bio = models.CharField(max_length=500, default="")
    picture = models.URLField(blank = True)
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