from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=100)
    duration = models.IntegerField()
    # poster = models.ImageField(upload_to='posters/')

    class Meta:
        ordering = ['genre']

    def __str__(self):
        return self.title



class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    available_seats = models.PositiveIntegerField()
    active = models.BooleanField(default=True)  # Add an 'active' field

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'{self.movie.title}'

    def is_past(self):
        now = timezone.make_naive(timezone.now())
        showtime_datetime = timezone.datetime.combine(self.date, self.time)
        return showtime_datetime < now


class Reservation(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat_number = models.PositiveIntegerField()

    class Meta:
        ordering = ['showtime__date', 'showtime__time']
        unique_together = ('showtime', 'seat_number')

    def __str__(self):
        return f'{self.user.username} - {self.showtime.movie.title} - {self.showtime.date} {self.showtime.time}'