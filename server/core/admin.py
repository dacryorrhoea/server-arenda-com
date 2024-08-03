from django.contrib import admin
from .models import Ad, Reservation, Review, Favorite, Rating

admin.site.register(Ad)
admin.site.register(Reservation)
admin.site.register(Review)
admin.site.register(Favorite)
admin.site.register(Rating)
