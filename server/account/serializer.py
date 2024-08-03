from rest_framework import  serializers
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from core.models import Ad, Reservation, Review, Favorite, BrowsingHistory
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password','first_name', 'last_name', 'email', 'groups')
        extra_kwargs = {
            'password':{'write_only': True},
        }

    def create(self, validated_data):
        groups_data = validated_data.pop('groups')
        user = User.objects.create_user(
            validated_data['username'],
            password = validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )

        for group_data in groups_data:
            user.groups.add(group_data)

        return user
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


# надо разобраться со гиперссылками...
class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        exclude = ['owner', 'id']

class AdForReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id', 'address']

class ReservationSerializer(serializers.ModelSerializer):
    ad = AdForReservationSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'begin_lease', 'end_lease', 'ad', 'lease_end_status']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

# class BrowsingHistorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model: BrowsingHistory
#         fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    owned_ads = AdSerializer(read_only=True, many=True)
    owned_reservations = ReservationSerializer(read_only=True, many=True)
    owned_reviews = ReviewSerializer(read_only=True, many=True)
    owned_favorites = FavoriteSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'groups',
            'owned_ads',
            'owned_reservations',
            'owned_reviews',
            'owned_favorites',
        ]

class ProfileSerializer(serializers.ModelSerializer):
    owned_ads = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'owned_ads',
            'owned_reviews',
        ]
