from django.db import models

# данные объявления
class Announcement(models.Model):
    # обязательная информация
    address = models.CharField(max_length=100)

    data_stay  = models.DateField(blank=True)
    data_leave = models.DateField(blank=True)

    member_adults = models.IntegerField()
    number_kids = models.IntegerField()
    animal_check = models.BooleanField()

    price = models.IntegerField()

    short_desc = models.CharField(max_length=100)
    description = models.TextField()
    
    # разобраться с соединением таблиц в моделях
    owner = models.IntegerField()

    # необязательная информация
    number_beds = models.IntegerField()
    type_housing = models.CharField(max_length=100)
    square_info = models.IntegerField()
    metro_info = models.CharField(max_length=100)
    img_src = models.CharField(max_length=100)
