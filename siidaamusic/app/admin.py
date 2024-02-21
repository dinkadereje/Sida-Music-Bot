from django.contrib import admin
from .models import Album,Track,Purchase
# Register your models here.
admin.site.register(Album)
admin.site.register(Track)
admin.site.register(Purchase)