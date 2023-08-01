import os
import django
import random
import datetime
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_reservation_system.settings')
django.setup()

from fav_movies.models import Movie, Showtime

def create_random_showtimes():
    movies = Movie.objects.all()
    max_showtimes_per_movie = 8  # You can adjust this value as needed

    for movie in movies:
        num_showtimes = random.randint(1, max_showtimes_per_movie)
        for _ in range(num_showtimes):
            date = timezone.now().date() + datetime.timedelta(days=random.randint(1, 30))
            time = datetime.time(random.randint(9, 23), 0)
            available_seats = random.choice([50, 100, 150, 200])

            showtime = Showtime.objects.create(movie=movie, date=date, time=time, available_seats=available_seats)

if __name__ == "__main__":
    create_random_showtimes()
    print("Random showtimes created successfully.", Showtime.objects.all())
