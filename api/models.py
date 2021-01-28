from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='person')
    age = models.PositiveSmallIntegerField()
    bio = models.CharField(max_length=255)

class Brand(models.Model):
    name = models.CharField(max_length=255)
    coverImage = models.CharField(max_length=360)
    logo = models.CharField(max_length=360)

class Product(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)
    price = models.IntegerField()
    image = models.CharField(max_length=255, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def no_of_ratings(self):
        ratings = Rating.objects.filter(product=self)
        return len(ratings)

    def avg_rating(self):
        sum = 0
        ratings = Rating.objects.filter(product=self)
        for rating in ratings:
            sum += rating.stars
        if len(ratings) > 0:
            return sum / len(ratings)
        else:
            return 0

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = (('user', 'product'))
        index_together = (('user', 'product'))
