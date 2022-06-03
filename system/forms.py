from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.forms import ModelForm
from .models import *


# Create User
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



# Create and Update Customer
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


# Create and Update Supplier
class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'


# Create and Update Warehouse
class WarehouseForm(ModelForm):
    class Meta:
        model = Warehouse
        fields = "__all__"

      
# Create and Update Category
class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        

# Create and Update Brand
class BrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'
        

# Create and Update Unit
class UnitForm(ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'
        

# Create and Update Expense_Category
class Expense_CategoryForm(ModelForm):
    class Meta:
        model = Expense_Category
        fields = '__all__'