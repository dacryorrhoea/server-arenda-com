from rest_framework import serializers
from .models import Ad, Reservation, Review, Favorite, Rating, BrowsingHistory
from django.contrib.auth.models import User
from drf_extra_fields.fields import DateRangeField


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'id']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['count_reviews', 'sum_rating']

class PublicViewReviewSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['owner', 'rating', 'text']


# сериализаторы для данных доступных только пользователям с нужными прaвами
class ReservationSerializer(serializers.ModelSerializer):
    ad = serializers.StringRelatedField(read_only=True)
    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'

class AdDetailSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    reservations = ReservationSerializer(many=True, read_only=True)
    reviews = PublicViewReviewSerializer(many=True, read_only=True)
    rating = RatingSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = '__all__'

    def create(self, validated_data):
        ad = Ad.objects.create(**validated_data)
        Rating.objects.create(ad=ad)
        return ad


class AdPartialSerializer(serializers.ModelSerializer):
    rating = RatingSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = ['id', 'address', 'price', 'short_desc', 'img_src', 'rating']


class FavoriteSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    ad = AdPartialSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = '__all__'

class BrowsingHistorySerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    ad = AdPartialSerializer(read_only=True)
    class Meta:
        model: BrowsingHistory
        fields = '__all__'
