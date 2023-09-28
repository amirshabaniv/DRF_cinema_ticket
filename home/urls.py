from rest_framework_nested import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()

router.register('actors', views.ActorViewSet) 
router.register('movies', views.MovieViewSet)
router.register('movie-comments', views.CommentViewSet)
router.register('contact-us', views.CallViewSet)

movie_router = routers.NestedDefaultRouter(router, "movies", lookup='movie')
movie_router.register("movie_ratings", views.MovieRatingViewSet, basename = "movie_rating")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(movie_router.urls))
]