from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class Album(models.Model):
    name=models.CharField(max_length=20)
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    total_track = models.IntegerField()
    language = models.CharField(max_length=50)
    release_date = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    global_price = models.DecimalField(max_digits=8, decimal_places=2)
    album_art = models.ImageField(upload_to='album_arts')
    
    def __str__(self):
        return self.name + " - " + self.artist.username  # Return
class Track(models.Model):
    name =models.CharField( max_length=50) 
    album = models.ForeignKey(Album,on_delete=models.CASCADE, related_name="tracks")   ## Foreign key to the parent model
    audio_file = models.FileField(upload_to="tracks", blank=True)
    duration = models.DurationField()
    track_number = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    global_price = models.DecimalField(max_digits=8, decimal_places=2)
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    track_art = models.ImageField(upload_to='track_arts')
    sample = models.FileField(upload_to="sample", blank=True)

    def __str__(self):
        return self.name + " - " + self.artist.username  # Return
class Purchase(models.Model):
    TYPE =(
        ('G','Global'),
        ('L','Local')
    )
    telegram_user_id = models.BigIntegerField()  # Store the Telegram user ID
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, null=True, blank=True)
    payment_type =  models.CharField(choices=TYPE, max_length=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Purchase {self.id} by {self.user.username} (Telegram ID: {self.telegram_user_id})"
    

    
    