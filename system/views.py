from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# ---------------------------------------------------------------------------------------------------------------
# Register Page
def register_page(request):
    if request.user.is_authenticated:
        return redirect('/system/dashboard')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'User was created for ' + user)            
                return redirect('/system/login_page')
    
        context = {'form' : form}
        return render(request, 'system/register_page.html', context)


# Login Page
def login_page(request):
    if request.user.is_authenticated:
        return redirect('/system/dashboard')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user     = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/system/dashboard')
            else:
                messages.info(request, 'Username or password is incorrect')
        
        context = {}
        return render(request, 'system/login_page.html', context)


# Logout User Functionality
def logout_user(request):
    logout(request)
    
    return redirect('login_page')
# ---------------------------------------------------------------------------------------------------------------

@login_required(login_url='login_page')
# Dashboard
def dashboard(request):
    
    return render(request, 'system/dashboard.html')

# ---------------------------------------------------------------------------------------------------------------

# Products List
@login_required(login_url='login_page')
def product_list(request):
    
    return render(request, 'system/product_list.html')


# Create Product
@login_required(login_url='login_page')
def create_product(request):
    
    return render(request, 'system/create_product.html')

# ---------------------------------------------------------------------------------------------------------------

# Customers List
@login_required(login_url='login_page')
def customer_list(request):
    customer_list  = Customer.objects.all()
    
    return render(request, 'system/customer_list.html', {'customer_list' : customer_list})


# Create Customer
@login_required(login_url='login_page')
def create_customer(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/system/customer_list')
        
    context = {'form' : form}
    return render(request, 'system/create_customer.html', context)

# Update Customer
@login_required(login_url='login_page')
def update_customer(request, pk):   
    customer = Customer.objects.get(id=pk)   
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/system/customer_list')
    
    context = {'form' : form}
    return render(request, 'system/create_customer.html', context)

# Delete Customer
@login_required(login_url='login_page')
def delete_customer(request, pk):    
    customer = Customer.objects.get(id=pk)   
    if request.method == "POST":
        customer.delete()
        return redirect('/system/customer_list')
    
    context = {'item' : customer}
    return render(request, 'system/delete_customer.html', context)

# ---------------------------------------------------------------------------------------------------------------

# Supplier List
@login_required(login_url='login_page')
def supplier_list(request):
    supplier_list = Supplier.objects.all()
    
    return render(request, 'system/supplier_list.html', {'supplier_list' : supplier_list})

# Create Supplier
@login_required(login_url='login_page')
def create_supplier(request):
    form = SupplierForm()
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/system/supplier_list')
        
    context = {'form' : form}   
    return render(request, 'system/create_Supplier.html', context)

# Update Supplier
@login_required(login_url='login_page')
def update_supplier(request, pk): 
    supplier = Supplier.objects.get(id=pk)   
    form = SupplierForm(instance=supplier)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('/system/supplier_list')
    
    context = {'form' : form}
    return render(request, 'system/create_supplier.html', context)

# Delete Supplier
@login_required(login_url='login_page')
def delete_supplier(request, pk): 
    supplier = Supplier.objects.get(id=pk)   
    if request.method == "POST":
        supplier.delete()
        return redirect('/system/supplier_list')
    
    context = {'item' : supplier}
    return render(request, 'system/delete_supplier.html', context)

# ---------------------------------------------------------------------------------------------------------------

# Warehouse List
@login_required(login_url='login_page')
def warehouse_list(request):
    warehouse_list = Warehouse.objects.all()
    
    return render(request, 'system/warehouse_list.html', {'warehouse_list' : warehouse_list})

# Create Warehouse
@login_required(login_url='login_page')
def create_warehouse(request):
    form = WarehouseForm()
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/system/warehouse_list')
        
    context = {'form' : form}   
    return render(request, 'system/create_warehouse.html', context)

# Update Warehouse
@login_required(login_url='login_page')
def update_warehouse(request, pk): 
    warehouse = Warehouse.objects.get(id=pk)   
    form = WarehouseForm(instance=warehouse)
    if request.method == 'POST':
        form = WarehouseForm(request.POST, instance=warehouse)
        if form.is_valid():
            form.save()
            return redirect('/system/warehouse_list')
    
    context = {'form' : form}
    return render(request, 'system/create_warehouse.html', context)

# Delete Warehouse
@login_required(login_url='login_page')
def delete_warehouse(request, pk): 
    warehouse = Warehouse.objects.get(id=pk)   
    if request.method == "POST":
        warehouse.delete()
        return redirect('/system/warehouse_list')
    
    context = {'item' : warehouse}
    return render(request, 'system/delete_warehouse.html', context)

# ---------------------------------------------------------------------------------------------------------------

# Category List
@login_required(login_url='login_page')
def category_list(request):
    category_list = Category.objects.all()
    
    return render(request, 'system/category_list.html', {'category_list' : category_list})

# Create Category
@login_required(login_url='login_page')
def create_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/system/category_list')
        
    context = {'form' : form}   
    return render(request, 'system/create_category.html', context)

# Update Category
@login_required(login_url='login_page')
def update_category(request, pk):
    category = Category.objects.get(id=pk)   
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('/system/category_list')
    
    context = {'form' : form}
    return render(request, 'system/create_category.html', context)

# Delete Category
@login_required(login_url='login_page')
def delete_category(request, pk): 
    category = Category.objects.get(id=pk)   
    if request.method == "POST":
        category.delete()
        return redirect('/system/category_list')
    
    context = {'item' : category}
    return render(request, 'system/delete_category.html', context)

# ---------------------------------------------------------------------------------------------------------------

# Brand List
@login_required(login_url='login_page')
def brand_list(request):
    brand_list  = Brand.objects.all()
    
    return render(request, 'system/brand_list.html', {'brand_list' : brand_list})

# Create Brand
@login_required(login_url='login_page')
def create_brand(request):
    form = BrandForm()
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/system/brand_list')
        
    context = {'form' : form}
    return render(request, 'system/create_brand.html', context)

# Update Brand
@login_required(login_url='login_page')
def update_brand(request, pk):   
    brand = Brand.objects.get(id=pk)   
    form = BrandForm(instance=brand)
    if request.method == 'POST':
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            return redirect('/system/brand_list')
    
    context = {'form' : form}
    return render(request, 'system/create_brand.html', context)

# Delete Brand
@login_required(login_url='login_page')
def delete_brand(request, pk):    
    brand = Brand.objects.get(id=pk)   
    if request.method == "POST":
        brand.delete()
        return redirect('/system/brand_list')
    
    context = {'item' : brand}
    return render(request, 'system/delete_brand.html', context)

# ---------------------------------------------------------------------------------------------------------------

# Unit List
@login_required(login_url='login_page')
def units_list(request):
    units_list = Unit.objects.all() 
    
    return render(request, 'system/units_list.html', {'units_list' : units_list})

# Create Unit
@login_required(login_url='login_page')
def create_unit(request):
    form = UnitForm()
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/system/units_list')
        
    context = {'form' : form}
    return render(request, 'system/create_unit.html', context)

# Update Unit
@login_required(login_url='login_page')
def update_unit(request, pk):   
    unit = Unit.objects.get(id=pk)   
    form = UnitForm(instance=unit)
    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('/system/units_list')
    
    context = {'form' : form}
    return render(request, 'system/create_unit.html', context)

# Delete Unit
@login_required(login_url='login_page')
def delete_unit(request, pk):    
    unit = Unit.objects.get(id=pk)   
    if request.method == "POST":
        unit.delete()
        return redirect('/system/units_list')
    
    context = {'item' : unit}
    return render(request, 'system/delete_unit.html', context)

# ---------------------------------------------------------------------------------------------------------------

# Expense Category
@login_required(login_url='login_page')
def expense_category_list(request):
    expense_category_list = Expense_Category.objects.all()
    
    return render(request, 'system/expense_category_list.html', {'expense_category_list' : expense_category_list})

@login_required(login_url='login_page')
def create_expense_category(request):
    form = Expense_CategoryForm()
    if request.method == 'POST':
        form = Expense_CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/system/expense_category_list')
        
    context = {'form' : form}
    return render(request, 'system/create_expense_category.html', context)

# Update Customer
@login_required(login_url='login_page')
def update_expense_category(request, pk):   
    expense_category = Expense_Category.objects.get(id=pk)   
    form = Expense_CategoryForm(instance=expense_category)
    if request.method == 'POST':
        form = Expense_CategoryForm(request.POST, instance=expense_category)
        if form.is_valid():
            form.save()
            return redirect('/system/expense_category_list')
    
    context = {'form' : form}
    return render(request, 'system/create_expense_category.html', context)

# Delete Customer
@login_required(login_url='login_page')
def delete_expense_category(request, pk):    
    expense_category = Expense_Category.objects.get(id=pk)   
    if request.method == "POST":
        expense_category.delete()
        return redirect('/system/expense_category_list')
    
    context = {'item' : expense_category}
    return render(request, 'system/delete_expense_category.html', context)

# ---------------------------------------------------------------------------------------------------------------

# Sales List
@login_required(login_url='login_page')
def sales_list(request):
    return render(request, 'system/sales_list.html')

# Create Sales
@login_required(login_url='login_page')
def create_sales(request):
    return render(request, 'system/create_sales.html')

# ---------------------------------------------------------------------------------------------------------------

# Purchase List
@login_required(login_url='login_page')
def purchase_list(request):
    return render(request, 'system/purchase_list.html')

# Create Purchase
@login_required(login_url='login_page')
def create_purchase(request):
    return render(request, 'system/create_purchase.html')

# ---------------------------------------------------------------------------------------------------------------

# Sales Return List
@login_required(login_url='login_page')
def sales_return_list(request):
    return render(request, 'system/sales_return_list.html')

# Create Sales Return
@login_required(login_url='login_page')
def create_sales_return(request):
    return render(request, 'system/create_sales_return.html')

# ---------------------------------------------------------------------------------------------------------------

# Purchase Return List
@login_required(login_url='login_page')
def purchase_return_list(request):
    return render(request, 'system/purchase_return_list.html')

# Create Purchase Return
@login_required(login_url='login_page')
def create_purchase_return(request):
    return render(request, 'system/create_purchase_return.html')

# ---------------------------------------------------------------------------------------------------------------

# Expense List
@login_required(login_url='login_page')
def expsense_list(request):
    return render(request, 'system/expenses_list.html')

# Create Expense
@login_required(login_url='login_page')
def create_expense(request):
    return render(request, 'system/create_expense.html')

# ---------------------------------------------------------------------------------------------------------------

# Report Payment Sales
@login_required(login_url='login_page')
def report_payment_sales(request):
    return render(request, 'system/report_payment_sales.html')

# Report Payment Sales Returns
@login_required(login_url='login_page')
def report_payment_sales_returns(request):
    return render(request, 'system/report_payment_sales_returns.html')

# Report Payment Purchases
@login_required(login_url='login_page')
def report_payment_purchases(request):
    return render(request, 'system/report_payment_purchases.html')

# Report Payment Purchases Returns
@login_required(login_url='login_page')
def report_payment_purchases_returns(request):
    return render(request, 'system/report_payment_purchases_returns.html')

# Report Product Quantity Alert
@login_required(login_url='login_page')
def report_product_quantity_alert(request):
    return render(request, 'system/report_product_quantity_alert.html')

# Report Top Selling Products
@login_required(login_url='login_page')
def report_top_selling_products(request):
    return render(request, 'system/report_top_selling_products.html')

# Report Best Customers
@login_required(login_url='login_page')
def report_best_customers(request):
    return render(request, 'system/report_best_customers.html')

# Create Expense Category
@login_required(login_url='login_page')
def create_expense_category(request):
    return render(request, 'system/create_expense_category.html')

# ---------------------------------------------------------------------------------------------------------------



