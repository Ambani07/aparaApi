from django.db import transaction
from rest_framework import serializers
from api.models import Product, Rating, Brand, Person
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class PersonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('age', 'bio')

class UserSerializers(serializers.ModelSerializer):
    person = PersonSerializers()
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'person')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    @transaction.atomic
    def create(self, validated_data):
        person_data = validated_data.pop('person')
        user = User.objects.create_user(**validated_data)
        user.person = Person.objects.create(user=user, **person_data)
        user.save()
        Token.objects.create(user=user)
        return user

class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name', 'coverImage', 'logo')


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'image', 'brand', 'user', 'no_of_ratings', 'avg_rating')


class RatingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'stars', 'user', 'product')
