from django.urls import path
from fav_movies import views
from django.contrib.auth.views import LogoutView

app_name = 'fav_movies'

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.MyLoginView.as_view(redirect_authenticated_user=True),name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='fav_movies:login'),name='logout'),
    path('accounts/register/', views.RegisterView.as_view(),name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:movie_id>/', views.movie_details, name='movie_details'),
    path('showtimes/', views.showtime_list, name='showtime_list'),
    path('showtimes/<int:showtime_id>/reserve/', views.reserve_seat, name='reserve_seat'),
    path('cancel/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('finished-shows', views.finished, name='finished'),
    path('search/', views.movie_search, name='movie_search'),
]