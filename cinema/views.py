from rest_framework.viewsets import ModelViewSet
from .models import Cinema, Schedule, CinemaRating, CinemaComment
from .serializers import CinemaSerializer, ScheduleSerializer, CinemaRatingSerializer, CinemaCommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


class CinemaViewSet(ModelViewSet):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['resturant', 'libary', 'buffet',
                        'cart_reader', 'ticket_print', 'accessible',
                        'coffe_shop', 'ATM', 'elevator', 'parking']
    search_fields = ['name']
    

class ScheduleViewSet(ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class CinemaRatingViewSet(ModelViewSet):
    serializer_class = CinemaRatingSerializer

    def get_queryset(self):
        return CinemaRating.objects.filter(cinema_id = self.kwargs['cinema_pk'])

    def get_serializer_context(self):
        user_id = self.request.user.id
        cinema_id = self.kwargs["cinema_pk"]
        return {"user_id": user_id, "cinema_id": cinema_id}


class CinemaCommentViewSet(ModelViewSet):
    queryset = CinemaComment.objects.all()
    serializer_class = CinemaCommentSerializer


