from rest_framework import serializers
from .models import Ad, Reservation, Review, Favorite, Rating, BrowsingHistory, PaymentReceipt, Image
from django.contrib.auth.models import User
from account.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class OwnerSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    owned_ads = serializers.StringRelatedField(read_only=True, many=True)
    owned_reservations = serializers.StringRelatedField(read_only=True, many=True)
    # reviews = PublicViewReviewSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'profile',
            'owned_ads',
            'owned_reservations',
        ]

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['count_reviews', 'sum_rating']




# сериализаторы для данных доступных только пользователям с нужными прaвами
class ReservationSerializer(serializers.ModelSerializer):
    ad = serializers.StringRelatedField(read_only=True)
    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'

class PublicViewReviewSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    reservation = ReservationSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['owner', 'rating', 'text', 'reservation']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['src']

class AdDetailSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    reservations = ReservationSerializer(many=True, read_only=True)
    reviews = PublicViewReviewSerializer(many=True, read_only=True)
    rating = RatingSerializer(read_only=True)
    images = ImageSerializer(read_only=True, many=True)

    class Meta:
        model = Ad
        fields = '__all__'

    def create(self, validated_data):
        ad = Ad.objects.create(**validated_data)
        Rating.objects.create(ad=ad)
        return ad


class AdPartialSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    rating = RatingSerializer(read_only=True)
    images = ImageSerializer(read_only=True, many=True)

    class Meta:
        model = Ad
        fields = [
            'id',
            'owner',
            'address',
            'address_lat',
            'address_lon',
            'min_length_of_stay',
            'max_length_of_stay',
            'price',
            'images',
            'fast_booking',
            'long_term',
            'cash_back',
            'short_desc',
            'rating',
            'type_flats',
            'square',
            'count_people',
            'count_beds'
        ]


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

class PaymentSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer(read_only=True)
    class Meta:
        model = PaymentReceipt
        fields = ['sum', 'reservation']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['address', 'address_lat', 'address_lon']
