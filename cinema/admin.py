from django.contrib import admin
from .models import Cinema, Schedule, PlayTime, DayAndDate, CinemaRating, CinemaComment


@admin.register(PlayTime)
class PlayTimeAdmin(admin.ModelAdmin):
    list_display = ['from_to', 'ticket_price']
    raw_id_fields = ['movie']

@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone']
    raw_id_fields = ['movie', 'play_time']

admin.site.register(DayAndDate) 

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['cinema']
    raw_id_fields = ['movie', 'cinema', 'day_and_date']

admin.site.register(CinemaRating)

admin.site.register(CinemaComment)