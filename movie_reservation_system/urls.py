"""
URL configuration for movie_reservation_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from fav_movies import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/login/', views.MyLoginView.as_view(redirect_authenticated_user=True),name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='login'),name='logout'),
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