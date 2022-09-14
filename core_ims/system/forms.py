from dataclasses import field
from django import forms
from enum import unique
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm

from .models import *


# Create User - Registration Form
class CreateUserForm(UserCreationForm):
    email       = forms.EmailField(widget=forms.EmailInput(attrs={'class' : 'input-field'}))
    first_name  = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'input-field'}))
    last_name   = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'input-field'}))
    
    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1',  'password2']
    
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class']  = 'input-field'
        self.fields['password1'].widget.attrs['class'] = 'input-field'
        self.fields['password2'].widget.attrs['class'] = 'input-field'


# Update User Info
class UpdateUserForm(forms.ModelForm):   
    username   = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'input_field'}))
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'input_field'}))
    last_name  = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'input_field'}))
    email      = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'input_field'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        

# Update User Profile
class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'phone', 'profile_pic', 'bio']
      

"""class AddPersonnelToGroupForm(forms.Form):
    personnels = forms.ModelMultipleChoiceField(
        queryset=Personnel.objects.all(),
        widget=forms.SelectMultiple(attrs={"class" : "form-control select-multiple"}))
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select(attrs={"class" : "form-control select-multiple"})
    )"""


# Reset Password
class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'pass-reset-inputfield',
        'placeholder': 'E-mail address',
        'type': 'email',
        'name': 'email'
        }))



# Create and Update Customer
class CustomerForm(ModelForm):
    class Meta:
        model  = Customer
        fields = ['code', 'name', 'phone', 'email', 'country', 'city', 'address', 'status', 'description']


# Create and Update Supplier
class SupplierForm(ModelForm):
    class Meta:
        model  = Supplier
        fields = ['code', 'name', 'phone', 'email', 'country', 'city', 'address', 'status', 'description']

       

# Create and Update Category
class CategoryForm(ModelForm):
    class Meta:
        model  = Category
        fields = ['code', 'name', 'description']
        

# Create and Update Brand
class BrandForm(ModelForm):
    class Meta:
        model  = Brand
        fields = ['code', 'name', 'description']
        

# Create and Update Unit
class UnitForm(ModelForm):
    class Meta:
        model  = Unit
        fields = ['code', 'name', 'unit_abbreviation', 'description' ]
        

#Create and Update Product
class ProductForm(ModelForm):
    # product_price  = models.DecimalField(max_digits=20, decimal_places=2)
    # product_cost   = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, null=True)
    product_price          = models.FloatField(default=0.00, null=True)
    product_cost           = models.FloatField(default=0.00, null=True)
    total_quantity = models.PositiveBigIntegerField(null=True, default=0)

    class Meta:
        model = Product
        fields = ['code', 'name', 'product_price', 'product_cost', 'total_quantity', 'product_unit', 'stock_alert', 'status', 'product_image', 'description', 'category', 'brand']
    
        
    def clean_product_price(self):
        product_price = self.cleaned_data.get('product_price')
        if product_price < 00.00:
            raise forms.ValidationError("Price has to be expressed in a positive numeric value")
        else:
            return product_price
        
        
    def clean_product_cost(self):
        product_cost = self.cleaned_data.get('product_cost')
        if product_cost < 00.00:
            raise forms.ValidationError("Cost has to be expressed in a positive numeric value")
        else:
            return product_cost
        
    
    def clean_total_quantity(self):
        total_quantity = self.cleaned_data.get('total_quantity')
        if total_quantity < 0:
            raise forms.ValidationError("Please enter positive numerical value for quantity")
        else:
            return total_quantity
    
    """def clean_product(self):
        product = self.cleaned_data.get("product")
        for instance in Product.objects.all():
            if instance.product == product:
                raise forms.ValidationError(product + 'is already created.')
        return product"""
        

# Create Sale
class SalesForm(forms.ModelForm):
    sales_quantity = models.PositiveBigIntegerField(blank=True, null=True, default=0)
    customer       = forms.ModelChoiceField(queryset=Customer.objects.filter(status="Active"))
    
    class Meta:
        model = Product
        fields = ['sales_quantity', 'customer', 'sales_note']
            
    def clean_sales_quantity(self):
        sales_quantity = self.cleaned_data.get('sales_quantity')
        if sales_quantity < 0:
            raise forms.ValidationError("You cannot sell negative quantity values")
        else:
            return sales_quantity

# Create Purchase
class PurchaseForm(forms.ModelForm):
    purchase_quantity = models.PositiveBigIntegerField(blank=True, null=True, default=0)
    supplier          = forms.ModelChoiceField(queryset=Supplier.objects.filter(status="Active"))
    
    class Meta:
        model = Product
        fields = ['purchase_quantity', 'supplier', 'purchase_note']
        
    def clean_purchase_quantity(self):
        purchase_quantity = self.cleaned_data.get('purchase_quantity')
        if purchase_quantity < 0:
            raise forms.ValidationError("You cannot purchase negative quantity values")
        else:
            return purchase_quantity
    
            
        
# Quantity Alert Report
# class QuantityAlertForm(ModelForm):
#     class Meta:
#         model = Product
#         fields = ['name', 'code', 'quantity', 'stock_alert' ]




















# ---------------------------------------------------------------------------------------------------------------
# !!! COMING SOON !!!

"""# Create and Update Expense_Category
class Expense_CategoryForm(ModelForm):
    class Meta:
        model  = Expense_Category
        fields = '__all__'"""
        

# Create and Update Warehouse
"""class WarehouseForm(ModelForm):
    class Meta:
        model  = Warehouse
        fields = "__all__"""

# Warehouse Adjustment - Add Product to Warehouse
"""class AdjustmentAddForm(ModelForm):
    class Meta:
        model  = AdjustmentAdd
        fields = '__all__'"""