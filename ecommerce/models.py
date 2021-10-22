from django.db import models
from django.db.models.fields import BooleanField
from django.contrib.auth.models import User

# Create your models here.

class users(models.Model):
    name = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=100)
    zip = models.IntegerField()

class Product(models.Model):
    productname = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    offer = BooleanField(default=False)
    active = BooleanField(default=False)
    image = models.ImageField(upload_to='pics/')
    
class Cart(models.Model):
    productname = models.CharField(max_length=100) 
    category = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.IntegerField()
    totalprice = models.IntegerField()
    pdtId = models.ForeignKey(Product, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

class Orders(models.Model):
    name = models.CharField(max_length=100) 
    phone = models.BigIntegerField(default=0)
    address = models.CharField(max_length=100) 
    address2 = models.CharField(max_length=100)
    district = models.CharField(max_length=50)
    zip = models.IntegerField(default=0)
    paymentMethod = models.CharField(max_length=20)
    products = models.CharField(max_length=100, default=0)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    category = models.CharField(max_length=50)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery = models.CharField(max_length=50)
    date = models.DateField()

class Comments(models.Model):
    name = models.CharField(max_length=100) 
    email = models.EmailField(max_length=254)
    phone = models.BigIntegerField()
    comment = models.CharField(max_length=100) 
    user = models.CharField(max_length=100) 
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

class Expenses(models.Model):
    FoodItems = models.BigIntegerField(default=0)
    Rent = models.BigIntegerField(default=0)
    Electricity = models.BigIntegerField(default=0)
    TotalSalary = models.BigIntegerField(default=0)
    OtherExpense = models.BigIntegerField(default=0)
    TotalExpense = models.BigIntegerField(default=0)
    CurrentDate = models.DateField()