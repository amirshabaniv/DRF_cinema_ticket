from rest_framework.viewsets import ModelViewSet
from .models import Actor, Movie, Comment, MovieRating, ContactUs
from .serializers import ActorSerializer, MovieSerializer, CommentSerializer, MovieRatingSerializer, ContactUsSerializer
from rest_framework import filters


class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    

class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class MovieRatingViewSet(ModelViewSet):
    serializer_class = MovieRatingSerializer

    def get_queryset(self):
        return MovieRating.objects.filter(movie_id = self.kwargs['movie_pk'])

    def get_serializer_context(self):
        user_id = self.request.user.id
        movie_id = self.kwargs["movie_pk"]
        return {"user_id": user_id, "movie_id": movie_id}
    

class CallViewSet(ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer

