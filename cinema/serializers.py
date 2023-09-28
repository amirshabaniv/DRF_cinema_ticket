from rest_framework import serializers
from .models import Cinema, PlayTime, DayAndDate, Schedule, CinemaRating, CinemaComment
from home.serializers import MovieSerializer
from statistics import mean


class PlayTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayTime
        fields = ['id', 'from_to', 'ticket_price', 'movie']


class DayAndDateSerializer(serializers.ModelSerializer):

    class Meta:
        model = DayAndDate
        fields = ['id', 'day_name', 'date_name']
    

class CinemaRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = CinemaRating
        fields = ["id", "rating", "description"]
    
    def create(self, validated_data):
        cinema_id = self.context["cinema_id"]
        user_id = self.context["user_id"]
        rating = CinemaRating.objects.create(cinema_id = cinema_id, user_id=user_id, **self.validated_data)
        return rating


class CinemaCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CinemaComment
        fields = ('id', 'user', 'body', 'cinema', 'created', 'comment_likes_count', 'comment_dislikes_count')


class CinemaSerializer(serializers.ModelSerializer):
    stars_avg = serializers.SerializerMethodField(method_name='avg_stars')
    play_time = PlayTimeSerializer(many=True)
    c_cinemacomments = CinemaCommentSerializer(many=True)
    
    class Meta:
        model = Cinema
        fields = ['id', 'name', 'movie', 'address','buffet', 'cart_reader', 'ticket_print',
                  'accessible', 'libary', 'resturant','coffe_shop', 'ATM', 'elevator', 'parking', 'image', 'description',
                  'phone', 'carwash', 'play_time', 'stars_avg', 'c_cinemacomments']
    
    def avg_stars(self, cinema:Cinema):
        items = cinema.c_ratings.all()
        if items.exists():
            avg = mean([item.rating for item in items])
            return avg
        return 0
    
    

class ScheduleSerializer(serializers.ModelSerializer):
    cinema = CinemaSerializer
    movie = MovieSerializer
    day_and_date = DayAndDateSerializer

    class Meta:
        model = Schedule
        fields = ['id', 'cinema', 'movie', 'day_and_date']


