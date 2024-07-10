from rest_framework import serializers
from .models import Ads

class AdsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = ('address', 'price', 'img_src', 'short_desc')

class AdsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = '__all__'
