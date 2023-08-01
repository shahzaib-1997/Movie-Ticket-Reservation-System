from django.test import TestCase, Client
from django.utils import timezone
from .models import Movie, Showtime, Reservation
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.

class MovieModelTestCase(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='This is a test movie.',
            genre='Action',
            duration=120,
        )

    def test_movie_creation(self):
        self.assertEqual(self.movie.title, 'Test Movie')
        self.assertEqual(self.movie.description, 'This is a test movie.')
        self.assertEqual(self.movie.genre, 'Action')
        self.assertEqual(self.movie.duration, 120)

    # Add more test methods for other model functionality if required


class ShowtimeModelTestCase(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='This is a test movie.',
            genre='Action',
            duration=120,
        )
        self.showtime = Showtime.objects.create(
            movie=self.movie,
            date=timezone.now().date(),
            time=timezone.now().time(),
            available_seats=100,
        )

    def test_showtime_creation(self):
        self.assertEqual(self.showtime.movie, self.movie)
        self.assertEqual(self.showtime.date, timezone.now().date())
        self.assertEqual(self.showtime.time, timezone.now().time())
        self.assertEqual(self.showtime.available_seats, 100)

    def test_is_active_property(self):
        # Add test cases for the 'is_active' property
        pass

    # Add more test methods for other model functionality if required


class ReservationModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='This is a test movie.',
            genre='Action',
            duration=120,
        )
        self.showtime = Showtime.objects.create(
            movie=self.movie,
            date=timezone.now().date(),
            time=timezone.now().time(),
            available_seats=100,
        )
        self.reservation = Reservation.objects.create(
            showtime=self.showtime,
            user=self.user,
            seat_number=1,
        )

    def test_reservation_creation(self):
        self.assertEqual(self.reservation.showtime, self.showtime)
        self.assertEqual(self.reservation.user, self.user)
        self.assertEqual(self.reservation.seat_number, 1)


# You can add more test classes for other models if you have them.
class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.movie = Movie.objects.create(title='Test Movie', description='This is a test movie.', genre='Action', duration=120)
        self.showtime = Showtime.objects.create(movie=self.movie, date='2023-07-05', time='15:00', available_seats=100)

    def test_home_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_movie_list_view(self):
        response = self.client.get('/movies/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Movie')

    def test_movie_details_view(self):
        response = self.client.get(reverse('movie_details', args=[self.movie.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Movie')

    def test_showtime_list_view(self):
        response = self.client.get('/showtimes/')
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_view_unauthenticated(self):
        response = self.client.get('/dashboard/')
        self.assertRedirects(response, '/accounts/login/?next=/dashboard/')
