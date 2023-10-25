from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.views.generic.edit import FormView
from .models import Movie, Showtime, Reservation
from .forms import RegisterForm
from django.core.paginator import Paginator
from django.core.mail import send_mail
from decouple import config

def home(request):
    return render(request, 'registration/home.html')

class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('fav_movies:login')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('fav_movies:dashboard')  # Redirect to the dashboard page if user is already authenticated
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        
        return super(RegisterView, self).form_valid(form)


class MyLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('fav_movies:dashboard') 

    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))

@login_required
def dashboard(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('showtime','showtime__date', 'showtime__time', 'seat_number')
    return render(request, 'fav_movies/dashboard.html', {'reservations': reservations})

def movie_list(request):
    movies = Movie.objects.all()
    paginator = Paginator(movies, 5)  # Display 5 movies per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'fav_movies/movie_list.html', {'page_obj': page_obj})

def movie_details(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    showtimes = Showtime.objects.filter(movie=movie)
    return render(request, 'fav_movies/movie_details.html', {'showtimes': showtimes, 'movie': movie})

def showtime_list(request):
    showtimes = Showtime.objects.all().order_by('date', 'time')
    active_showtimes = [showtime for showtime in showtimes if showtime.is_active]
    paginator = Paginator(active_showtimes, 10)  # Display 10 showtimes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'fav_movies/showtime_list.html', {'page_obj': page_obj})

@login_required
def reserve_seat(request, showtime_id):
    showtime = Showtime.objects.get(id=showtime_id)
    reservations = Reservation.objects.filter(showtime=showtime)
    seat_numbers = [reservation.seat_number for reservation in reservations]

    if request.method == 'POST':
        selected_seats = [int(seat_number) for seat_number in request.POST.getlist('seat_number') if seat_number]

        if selected_seats:
            for seat_number in selected_seats:
                Reservation.objects.create(showtime=showtime, user=request.user, seat_number=seat_number)
            
            send_mail(
                'Reservation Confirmation',
                f'Thank you for reserving seat for {showtime.movie.title} on {showtime.date} at {showtime.time}.\nYour reserved seats: {selected_seats}.',
                config("EMAIL"),
                [request.user.email],
                fail_silently=False,
            )
        else:
            messages.error(request,'No seat selected')
            
        return redirect('fav_movies:reserve_seat', showtime_id=showtime_id)


    reserves = Reservation.objects.filter(user=request.user, showtime=showtime)
    user_seats = [reservation.seat_number for reservation in reserves]
    context = {
        'showtime': showtime, 
        'seats': range(1,showtime.available_seats+1),
        'seat_numbers': seat_numbers,
        'user_seats' : user_seats
    }

    return render(request, 'fav_movies/reserve_seat.html', context)

@login_required
def cancel_reservation(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    if request.method == 'POST':
        reservation.delete()
        return redirect('fav_movies:dashboard')
    return render(request, 'fav_movies/cancel_reservation.html', {'reservation': reservation})

@login_required
def finished(request):
    all_reservations = Reservation.objects.filter(user=request.user).order_by('showtime', 'seat_number')
    reservations = [reservation for reservation in all_reservations if not reservation.showtime.is_active]
    return render(request, 'fav_movies/finished.html', {'reservations': reservations})


def movie_search(request):

    if request.GET.get('query'):
        query = request.GET.get('query')
        movies = Movie.objects.filter(title__icontains=query)

        return render(request, 'fav_movies/movie_search.html', {'movies': movies,})

    return redirect('fav_movies:dashboard')
