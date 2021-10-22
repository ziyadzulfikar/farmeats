from django.contrib import admin

from .models import Product, users

# Register your models here.

admin.site.register(users)
admin.site.register(Product)