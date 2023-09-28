from rest_framework import serializers
from .models import Actor, Movie, Comment, MovieRating, ContactUs
from statistics import mean


class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = ['id', 'name', 'description', 'image1', 'image2', 'image3', 'image4']


class MovieRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieRating
        fields = ["id", "rating", "description"]
    
    def create(self, validated_data):
        movie_id = self.context["movie_id"]
        user_id = self.context["user_id"]
        rating = MovieRating.objects.create(movie_id = movie_id, user_id=user_id, **self.validated_data)
        return rating


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'user', 'body', 'movie', 'created', 'comment_likes_count', 'comment_dislikes_count')


class MovieSerializer(serializers.ModelSerializer):
    stars_avg = serializers.SerializerMethodField(method_name='avg_stars')
    m_comments = CommentSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'name','director', 'description', 'category', 'genre',
                 'actor', 'slug', 'image1', 'image2', 'image3', 'image4', 'stars_avg', 'm_comments']
        
    def avg_stars(self, movie:Movie):
        items = movie.m_ratings.all()
        if items.exists():
            avg = mean([item.rating for item in items])
            return avg
        return 0


class ContactUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactUs
        fields = ['phone_number', 'fax', 'email', 'address']
        





