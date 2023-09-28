from rest_framework_nested import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()

router.register('cinemas', views.CinemaViewSet)
router.register('schedules', views.ScheduleViewSet)
router.register('cinema-comments', views.CinemaCommentViewSet)

cinema_router = routers.NestedDefaultRouter(router, "cinemas", lookup='cinema')
cinema_router.register("cinema_ratings", views.CinemaRatingViewSet, basename = "cinema_rating")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(cinema_router.urls)),
]