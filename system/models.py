from distutils.command.upload import upload
import email
from pyexpat import model
from tabnanny import verbose
from types import CoroutineType
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# ---------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------
# Customers
class Customer(models.Model):
    name         = models.CharField(max_length=200, unique=True)
    code         = models.CharField(max_length=20, unique=True)
    phone        = models.CharField(max_length=30, unique=True)
    email        = models.CharField(max_length=50, unique=True)
    country      = models.CharField(max_length=50)
    city         = models.CharField(max_length=50)
    address      = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

# --------------------------------------------------------------------------------------------------------------- 
# Suppliers
class Supplier(models.Model):
    name         = models.CharField(max_length=200, unique=True)
    code         = models.CharField(max_length=20, unique=True)
    phone        = models.CharField(max_length=30, unique=True)
    email        = models.CharField(max_length=50, unique=True)
    country      = models.CharField(max_length=50)
    city         = models.CharField(max_length=50)
    address      = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return self.name
    
# ---------------------------------------------------------------------------------------------------------------   
# Warehouses
class Warehouse(models.Model):
    name         = models.CharField(max_length=200, unique=True)
    code         = models.CharField(max_length=20, unique=True)
    phone        = models.CharField(max_length=30, unique=True)
    email        = models.CharField(max_length=50, unique=True)
    country      = models.CharField(max_length=50)
    city         = models.CharField(max_length=50)
    address      = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return self.name

# ---------------------------------------------------------------------------------------------------------------
# Categories (of Products)
class Category(models.Model):
    code         = models.CharField(max_length=200, unique=True)
    name         = models.CharField(max_length=200, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    def __str__(self):
        return self.name
    
# ---------------------------------------------------------------------------------------------------------------    
# Brands
class Brand(models.Model):
    code         = models.CharField(max_length=200, unique=True)
    name         = models.CharField(max_length=200, unique=True)
    brand_image  = models.ImageField(upload_to="images/brands", blank=True, null=True)
    description  = models.CharField(max_length=300, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return self.name

# ---------------------------------------------------------------------------------------------------------------
# Units
class Unit(models.Model):
    code                 = models.CharField(max_length=20, unique=True)
    name                 = models.CharField(max_length=200, unique=True)
    base_unit            = models.CharField(max_length=30)
    unit_abbreviation    = models.CharField(max_length=50, unique=True)
    unit_operator        = models.CharField(max_length=50)
    unit_operation_value = models.CharField(max_length=50)
    date_created         = models.DateTimeField(auto_now_add=True)
    date_updated         = models.DateTimeField(auto_now_add=True)
    date_deleted         = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return self.name

# ---------------------------------------------------------------------------------------------------------------
# Expense Category
class Expense_Category(models.Model):
    code         = models.CharField(max_length=200, unique=True)
    name         = models.CharField(max_length=200, unique=True)
    description  = models.CharField(max_length=300, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'expense_category'
        verbose_name_plural = 'expense_categories'
       
    def __str__(self):
        return self.name
    
# ---------------------------------------------------------------------------------------------------------------   
# # Products
"""class Product(models.Model):
    name         = models.CharField(max_length=200, unique=True)
    code         = models.CharField(max_length=20, unique=True)
    category     = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand        = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    product_cost = models.DecimalField(max_digits=20, decimal_places=2)
    product_price = models.DecimalField(max_digits=20, decimal_places=2)
    product_unit  = models.ForeignKey(Unit, on_delete=models.CASCADE)
    purchase_unit  = models.ForeignKey(Unit, on_delete=models.CASCADE)
    sales_unit  = models.ForeignKey(Unit, on_delete=models.CASCADE)
    stock_alert = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name""" 

# ---------------------------------------------------------------------------------------------------------------    
# # Sales
# class Sale(models.Model):
#     name         = models.CharField(max_length=200, unique=True)
#     code         = models.CharField(max_length=20, unique=True)
#     category     = models.ForeignKey(Category, on_delete=models.CASCADE)
#     brand        = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
#     product_cost = models.DecimalField(max_digits=20, decimal_places=2)
#     product_price = models.DecimalField(max_digits=20, decimal_places=2)
#     product_unit  = models.ForeignKey(Unit, on_delete=models.CASCADE)
#     purchase_unit  = models.ForeignKey(Unit, on_delete=models.CASCADE)
#     sales_unit  = models.ForeignKey(Unit, on_delete=models.CASCADE)
#     stock_alert = models.IntegerField(blank=True, null=True)
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_updated = models.DateTimeField(auto_now_add=True)
#     date_deleted = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.name
#     def __str__(self):
#         return str(self.name) + ": $" + str(self.product_price)