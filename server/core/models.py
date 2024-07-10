from django.db import models

# данные объявления
class Ads(models.Model):
    # поля которые будут использоваться для фильтрации
    address = models.CharField(max_length=100)

    number_people = models.IntegerField() # количество гостей
    number_beds_one = models.IntegerField() # количество одноместных кроватей
    number_beds_two = models.IntegerField() # количество двуместных кроватей
    animal_check = models.BooleanField()

    price = models.IntegerField()
    square_info = models.IntegerField()
    type_housing = models.CharField(max_length=100)

    # поля с описанием и подобное
    time_stay  = models.CharField(max_length=100)
    time_leave = models.CharField(max_length=100)
    short_desc = models.CharField(max_length=100)
    description = models.TextField()
    
    # owner для указания ключа на владельца объявления
    # и ссылка на изображение, для которых потом надо реализовать media
    owner = models.IntegerField()
    img_src = models.CharField(max_length=100)
