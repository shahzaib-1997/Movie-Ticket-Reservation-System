from django.contrib import admin
from .models import Movie, Showtime, Reservation

# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):

    list_display = ["title", "genre", "duration"]

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):

    list_display = ["movie", "available_seats", "date", "time"]

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    list_display = ["user", "showtime", "showtime_date", "showtime_time", "seat_number"]

    def showtime_date(self, obj):
        return obj.showtime.date

    def showtime_time(self, obj):
        return obj.showtime.time

    showtime_date.short_description = "Showtime Date"
    showtime_time.short_description = "Showtime Time"

