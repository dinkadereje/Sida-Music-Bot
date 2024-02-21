from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .views import AlbumViewSet, TrackViewSet,AlbumTracksView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'albums', AlbumViewSet, basename='album')
router.register(r'tracks', TrackViewSet, basename='track')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/albums/<int:album_id>/tracks/', AlbumTracksView.as_view(), name='album-tracks'),

]