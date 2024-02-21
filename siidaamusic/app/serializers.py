from rest_framework import serializers
from .models import Purchase, Album, Track

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'

class PurchaseSerializer(serializers.ModelSerializer):
    album = AlbumSerializer(required=False)  # Serialize the related Album model
    track = TrackSerializer(required=False)  # Serialize the related Track model

    class Meta:
        model = Purchase
        fields = '__all__'

    def create(self, validated_data):
        # Extract album and track data from the validated data
        album_data = validated_data.pop('album', None)
        track_data = validated_data.pop('track', None)

        # Create or retrieve the related Album and Track instances
        album_instance = Album.objects.create(**album_data) if album_data else None
        track_instance = Track.objects.create(**track_data) if track_data else None

        # Create the Purchase instance with the related Album and Track
        purchase_instance = Purchase.objects.create(album=album_instance, track=track_instance, **validated_data)

        return purchase_instance
