from django.contrib import admin

# Register your models here.
from api.models import Brand, Product, Rating, Person

admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Rating)
admin.site.register(Person)
