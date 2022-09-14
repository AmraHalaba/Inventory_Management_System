from email.policy import default
from tabnanny import verbose
from tkinter import CASCADE
from django.contrib.auth.models import User
from django.db.models import Sum

from django.db import models


# ---------------------------------------------------------------------------------------------------------------
# User
class UserProfile(models.Model):
    client       = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    role         = models.CharField(max_length=200, null=True)
    phone        = models.CharField(max_length=200, unique=True, null=True)
    profile_pic  = models.ImageField(default='default.png', null=True, blank=True, upload_to='profile_images')
    bio          = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f'{self.client.username} Profile'

# ---------------------------------------------------------------------------------------------------------------
# Customers
class Customer(models.Model):
    STATUSES = (
                ("ACTIVE",   "Active"),
                ("INACTIVE", "Inactive")
    )
    
    # Basic Fields
    code         = models.CharField(max_length=20, unique=True)
    name         = models.CharField(max_length=200, unique=True)
    phone        = models.CharField(max_length=30, unique=True)
    email        = models.CharField(max_length=50, unique=True)
    country      = models.CharField(max_length=50)
    city         = models.CharField(max_length=50)
    address      = models.CharField(max_length=200)
    status       = models.CharField(max_length=20, null=True, choices=STATUSES, default="ACTIVE")
    description  = models.TextField(max_length=300, blank=True, null=True)
    
    # Utility Fields
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.name

# --------------------------------------------------------------------------------------------------------------- 
# Suppliers
class Supplier(models.Model):
    STATUSES = (
                ("ACTIVE",   "Active"),
                ("INACTIVE", "Inactive")
    )
    
    # Basic Fields
    code         = models.CharField(max_length=20, unique=True)
    name         = models.CharField(max_length=200, unique=True)
    phone        = models.CharField(max_length=30, unique=True)
    email        = models.CharField(max_length=50, unique=True)
    country      = models.CharField(max_length=50)
    city         = models.CharField(max_length=50)
    address      = models.CharField(max_length=200)
    status       = models.CharField(max_length=20, null=True, choices=STATUSES, default="ACTIVE")
    description  = models.TextField(max_length=300, blank=True, null=True)
    
    # Utility Fields
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
# ---------------------------------------------------------------------------------------------------------------   

# Categories (of Products)
class Category(models.Model):
    # Basic Fields
    code         = models.CharField(max_length=200, unique=True)
    name         = models.CharField(max_length=200, unique=True)
    description  = models.TextField(max_length=300, blank=True, null=True)
    
    # Utility Fields
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    def __str__(self):
        return self.name
    
#  ---------------------------------------------------------------------------------------------------------------    
# Brands
class Brand(models.Model):
    # Basic Fields
    code         = models.CharField(max_length=200, unique=True)
    name         = models.CharField(max_length=200, unique=True)
    description  = models.TextField(max_length=300, blank=True, null=True)
    
    #Utility Fields
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return self.name

# ---------------------------------------------------------------------------------------------------------------
# Units
class Unit(models.Model):
    # Basic Fields
    code                 = models.CharField(max_length=20, unique=True)
    name                 = models.CharField(max_length=200, unique=True)
    unit_abbreviation    = models.CharField(max_length=50, unique=True)
    description          = models.TextField(max_length=300, blank=True, null=True)
     
    # Utility Fields
    date_created         = models.DateTimeField(auto_now_add=True)
    date_updated         = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return self.name

# ---------------------------------------------------------------------------------------------------------------   
# Set default values of choices for category, brand, and unit --> will: get a default value for the object; create a new value if not available
def get_default_category():
    return Category.objects.get_or_create(name="Generic product")[0]

def get_default_brand():
    return Brand.objects.get_or_create(name="Generic product")[0]

def get_default_product_unit():
    return Unit.objects.get_or_create(name="Piece")[0]

def get_walkin_customer():
    return Customer.objects.get_or_create(name="Walk-in customer")[0]

def get_generic_supplier():
    return Supplier.objects.get_or_create(name="Generic supplier")[0]

# Products
class Product(models.Model):
    STATUSES = (
                ("ACTIVE",   "Active"),
                ("INACTIVE", "Inactive")
    )
    
    # Basic Fields
    code                   = models.CharField(max_length=20, unique=True)
    name                   = models.CharField(max_length=200, unique=True)  
    # product_price          = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    # product_cost           = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, null=True)
    product_price          = models.FloatField(default=0.00, null=True)
    product_cost           = models.FloatField(default=0.00, null=True)
    total_quantity         = models.PositiveBigIntegerField(null=True, default=0)
    stock_alert            = models.IntegerField(blank=True, null=True)
    status                 = models.CharField(max_length=20, null=True, choices=STATUSES, default="ACTIVE")
    product_image          = models.ImageField(blank=True, null=True, upload_to='product_images/')
    description            = models.TextField(max_length=300, blank=True, null=True)
    sales_quantity         = models.PositiveBigIntegerField(blank=True, null=True, default=0)
    purchase_quantity      = models.PositiveBigIntegerField(blank=True, null=True, default=0)
    sales_created_by       = models.CharField(max_length=100, blank=True, null=True)
    purchase_created_by    = models.CharField(max_length=100, blank=True, null=True)
    sales_note             = models.TextField(max_length=300, blank=True, null=True)
    purchase_note          = models.TextField(max_length=300, blank=True, null=True)

    # Related Fields
    product_unit           = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, default=get_default_product_unit)
    category               = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, default=get_default_category)
    brand                  = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True, default=get_default_brand) 
    customer               = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, default=get_walkin_customer)
    supplier               = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True, default=get_generic_supplier)
    
    # Utility Fields
    date_created           = models.DateTimeField(auto_now_add=True)
    date_updated           = models.DateTimeField(auto_now=True)
            
    def __str__(self):
        return self.name
    
    @property 
    def total_sale_per_product(self):
        total_sales_amount_per_product = self.product_price * self.sales_quantity
        return total_sales_amount_per_product
    
    @property 
    def total_revenue_per_product(self):
        total_revenue_product = (self.product_price * self.sales_quantity) - (self.product_cost * self.sales_quantity)
        return total_revenue_product
    
    @property 
    def total_revenue_overall(self):
        #total_revenue_product = sum( (self.product_price * self.sales_quantity) - (self.product_cost * self.sales_quantity) )
        total_revenue_product = Sum( (self.product_price * self.sales_quantity) - (self.product_cost * self.sales_quantity) )
        return total_revenue_product
  
        
    
    # @property 
    # def total_sales(self):
    #     total_sales_amount = 0
    #     #total_sales_amount += sum(self.product_price * self.sales_quantity)
    #     total_sales_amount = sum(self.product_price) * sum(self.sales_quantity)
    #     return total_sales_amount
    
    



# ---------------------------------------------------------------------------------------------------------------    











# ---------------------------------------------------------------------------------------------------------------
### !!! COMING SOON !!! ###
# ---------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------
# Warehouse Adjustment - Adding Products to Warehouse   
"""class AdjustmentAdd(models.Model):
    warehouse  = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True)
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity   = models.PositiveBigIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "Adjustment " + str(self.id)
    
    def __str__(self):
    	return ("%s , %s " (self.product.name,self.warehouse.name))"""
     
# ---------------------------------------------------------------------------------------------------------------
# Expense Category
"""class Expense_Category(models.Model):
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
        return self.name"""


# ---------------------------------------------------------------------------------------------------------------  
# Warehouses
"""class Warehouse(models.Model):
    name         = models.CharField(max_length=200, unique=True)
    code         = models.CharField(max_length=20, unique=True)
    phone        = models.CharField(max_length=30, unique=True)
    email        = models.CharField(max_length=50, unique=True)
    country      = models.CharField(max_length=50)
    city         = models.CharField(max_length=50)
    address      = models.CharField(max_length=200)
    description  = models.TextField(max_length=300, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return self.name"""

# ---------------------------------------------------------------------------------------------------------------    
# Sales
"""class Sale(models.Model):
    name          = models.CharField(max_length=200, unique=True)
    code          = models.CharField(max_length=20, unique=True)
    category      = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand         = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    product_price = models.DecimalField(max_digits=20, decimal_places=2)
    staff         = models.ForeignKey(User, null=True, on_delete=models.CASCADE) #this will "call" from Django generated User model, that is it will pick a user created by registration
    #sales_unit    = models.ForeignKey(Unit, related_name="sales_unit", on_delete=models.CASCADE, null=True)
    date_created  = models.DateTimeField(auto_now_add=True)
    date_updated  = models.DateTimeField(auto_now_add=True)
    date_deleted  = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.name) + ": $" + str(self.product_price) + "created_by: " + (self.staff.username)"""

# ---------------------------------------------------------------------------------------------------------------    
# Purchases
"""class Purchase(models.Model):
    pass"""

# ---------------------------------------------------------------------------------------------------------------    
# Sales Returns
"""class SaleReturns(models.Model):
    pass"""

# ---------------------------------------------------------------------------------------------------------------    
# Purchase Returns
"""class PurchaseReturns(models.Model):
    pass"""

# ---------------------------------------------------------------------------------------------------------------    
# Expenses
"""class Expense(models.Model):
    pass"""
