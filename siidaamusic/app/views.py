# views.py
from rest_framework import viewsets
from .models import Album, Track
from rest_framework.generics import ListAPIView
from .serializers import AlbumSerializer, TrackSerializer

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
class AlbumTracksView(ListAPIView):
    serializer_class = TrackSerializer

    def get_queryset(self):
        album_id = self.kwargs.get('album_id')

        queryset = Track.objects.filter(album_id = album_id)
        return queryset
    
