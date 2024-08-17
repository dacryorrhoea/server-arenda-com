from django.contrib import admin
from .models import Ad, Reservation, Review, Favorite, Rating, PaymentReceipt

admin.site.register(Ad)
admin.site.register(Reservation)
admin.site.register(Review)
admin.site.register(Favorite)
admin.site.register(Rating)
admin.site.register(PaymentReceipt)
