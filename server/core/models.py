from django.db import models
from django.contrib.auth.models import User


class Ad(models.Model):
    description = models.TextField()
    img_src = models.CharField(max_length=300)
    clock_entry = models.CharField(max_length=100)
    clock_leave = models.CharField(max_length=100)
    min_length_of_stay = models.IntegerField()
    max_length_of_stay = models.IntegerField()
    animal_check = models.BooleanField()
    smoking_check = models.BooleanField()
    party_check = models.BooleanField()
    docs_check = models.BooleanField()
    kids_check = models.BooleanField()
    wifi = models.BooleanField()
    drier = models.BooleanField()
    towel = models.BooleanField()
    bed_linen = models.BooleanField()
    tv = models.BooleanField()
    microwave = models.BooleanField()
    electric_kettle = models.BooleanField()
    balcony = models.BooleanField()
    params = models.CharField(max_length=200)
    count_beds = models.IntegerField()
    square = models.IntegerField()
    count_people = models.IntegerField()
    sleeping_places = models.IntegerField()
    beds_info = models.CharField(max_length=200)
    type_flats = models.CharField(max_length=200)
    short_desc = models.TextField()
    address = models.CharField(max_length=200)
    price = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_ads')

    def __str__(self):
        return self.address

    
class Reservation(models.Model):
    begin_lease = models.DateField()
    end_lease = models.DateField()

    approve_status = models.BooleanField(default=True)
    lease_end_status = models.BooleanField(default=False)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_reservations')

    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='reservations')

    def __str__(self):
        return f'бронь на {str(self.begin_lease)} - {str(self.end_lease)}, для объявления: {self.ad}'


class Rating(models.Model):
    count_reviews = models.IntegerField(default=0)
    sum_rating = models.IntegerField(default=0)

    ad = models.OneToOneField(Ad, on_delete = models.CASCADE, primary_key = True)

    def __str__(self):
        return f'Рейтинг объявления: {self.ad}'


class Review(models.Model):
    text = models.TextField()
    rating = models.IntegerField()

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_reviews')

    reservation = models.OneToOneField(Reservation, on_delete = models.CASCADE, primary_key = True)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f'Отзыв на объявление: {self.ad}'


class Favorite(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_favorites')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='users_has_as_favorite')

    def __str__(self):
        return f'Избранное пользователя: {self.owner}'
    

class BrowsingHistory(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_browsing_history')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='users_has_as_browsing_history')

    def __str__(self):
        return f'История посещений пользователя: {self.owner}'

