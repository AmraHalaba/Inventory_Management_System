from multiprocessing import context
from telnetlib import STATUS
from urllib import response
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.core.paginator import Paginator
import csv 
#from django_pandas.io import read_frame
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Sum

# from rest_framework.views import APIView
# from rest_framework.response import Response


from .models import *
from .forms import *
from .decorators import *

# Header - Report Product Quantity Alert Badge Notification
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def header(request):
    all_products = Product.objects.all()

    context = { 'all_products' : all_products}    
    return render(request, 'system/includes/header.html', context)





# ---------------------------------------------------------------------------------------------------------------
# Register Page
@unauthenticated_user
def register_page(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user     = form.save()
            username = form.cleaned_data.get('username')
            group    = Group.objects.get(name='Staff - Level 2')
            user.groups.add(group)
            messages.success(request, 'Account was created for ' + username)            
            return redirect('/system/login_page')

    context = {'form' : form}
    return render(request, 'system/register_page.html', context)


# Login Page
@unauthenticated_user
def login_page(request):
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
# Users List
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager'])
def users_list(request):    
    user_list  = get_user_model().objects.all()
    #group_list = Group.objects.all()
    #print('grupe: ', group_list)
    
    #Search Bar
    if request.method == "POST":
        searched  = request.POST['searched']
        user_list = get_user_model().objects.filter(last_name__icontains=searched)
        # Pagination
        pag        = Paginator(user_list, 5)
        page       = request.GET.get('page')
        page_items = pag.get_page(page)
        
        context = { 'user_list' : user_list,
                    'page_items'   : page_items}
        return render(request, 'system/users_list.html', context)
    else:
        user_list = get_user_model().objects.all()
        # Pagination
        pag        = Paginator(user_list, 5)
        page       = request.GET.get('page')
        page_items = pag.get_page(page)
        
        context = { 'user_list' : user_list,
                    'page_items'   : page_items}
        return render(request, 'system/users_list.html', context)

# Export Users List into CSV
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def users_list_csv(request):
    response                        = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="list_of_users.csv"'
    writer                          = csv.writer(response)
    users_list                      = get_user_model().objects.all()

    writer.writerow( [ 'First Name', 'Last Name', 'Username', 'Email' ] )

    for user in users_list:
        writer.writerow( [ user.first_name , user.last_name , user.username , user.email , ] )
    
    return response

# ---------------------------------------------------------------------------------------------------------------
# User Profile Page
@login_required(login_url='login_page')
def user_page(request):    
    context = {}
    return render(request, 'system/user_page.html', context)

# ---------------------------------------------------------------------------------------------------------------
# User Profile Page Settings
@login_required(login_url='login_page')
def user_settings(request): #dodati pk u parametre (request, pk)
    #userprofile = UserProfile.objects.get(id=pk)
    #user_form = UserProfileForm(request.POST, instance=userprofile)
    if request.method =="POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile is updated")
            return redirect('/system/user_page')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateUserProfileForm(instance=request.user.userprofile)
        messages.error(request, "There is an error, try again")
       
    context = {'user_form' : user_form, 'profile_form' : profile_form}
    return render(request, 'system/user_settings.html', context)

# ---------------------------------------------------------------------------------------------------------------
# Dashboard
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def dashboard(request):
    products  = Product.objects.all()
    suppliers = Supplier.objects.all()
    customers = Customer.objects.all()
    
    total_products  = products.filter(status='ACTIVE').count()
    total_suppliers = suppliers.filter(status='ACTIVE').count()
    total_customers = customers.filter(status='ACTIVE').count()
    
    top_selling_products = products.filter(status='ACTIVE').order_by('-sales_quantity')[:5]
    
    # for product in top_selling_products:
    #     print(product)
    
    #total_revenue = Product.objects.filter(customer=total_customers,).aggregate(total_revenue=Sum("sales_quantity__product_price"))["sales_quantity"]
    
    context = { 'products'             : products,
                'suppliers'            : suppliers,
                'customers'            : customers,
                'total_products'       : total_products,
                'total_suppliers'      : total_suppliers,
                'total_customers'      : total_customers,
                'top_selling_products' : top_selling_products}
    return render(request, 'system/dashboard.html', context)



# ---------------------------------------------------------------------------------------------------------------
# Stock
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def stock(request):
    product_list = Product.objects.all().filter(status="Active")
    #product_list = Product.objects.filter(status="Active")
    #product_list = Product.objects.filter(status="Active").value
    #product_list = Product.objects.raw('SELECT * FROM system_product WHERE status="ACTIVE"')
    #print("raw sql query: ", product_list)
    
   #product_list = Product.objects.all()
    #print("STATUSI", product_list.status)
    
    #Search Bar
    if request.method == "POST":
        searched = request.POST['searched']
        product_list = Product.objects.filter(name__icontains=searched)
        
    
        # Pagination
        pag        = Paginator(product_list, 5)
        page       = request.GET.get('page')
        page_items = pag.get_page(page)
        
        context = { 'product_list' : product_list,
                    'page_items'   : page_items}
        return render(request, 'system/stock.html', context)
    else:
        product_list = Product.objects.all().filter(status="Active")
        
        # Pagination
        pag        = Paginator(product_list, 5)
        page       = request.GET.get('page')
        page_items = pag.get_page(page)
        
        context = { 'product_list' : product_list,
                    'page_items'   : page_items}
        return render(request, 'system/stock.html', context)

# Export Products List into CSV
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def stock_list_csv(request):
    response                        = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products_on_stock.csv"'
    writer                          = csv.writer(response)
    stock_list                      = Product.objects.all()

    writer.writerow( [ 'Product Code', 'Product Name', 'Category', 'Brand', 'Total Qty', 'Product Unit', 'Stock Alert Qty', 'Status', 'Description', 'Date created' ] )

    for product in stock_list:
        writer.writerow( [ product.code, product.name, product.category, product.brand, product.product_price, product.total_quantity, product.stock_alert, product.status, product.description, product.date_created ] )
    
    return response


# Stock Detail Page
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def stock_detail(request, pk):
    stock_detail = Product.objects.filter(id=pk)
    
    context = {'stock_detail' : stock_detail}
    return render(request, 'system/stock_details.html', context)

# Product Sales
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1'])
def product_sales(request, pk):
    product   = Product.objects.get(id=pk)
    customers = Customer.objects.all()
    form      = SalesForm(request.POST or None, instance=product)
    
    #if product.status=="Active" and customers.status=="Active":
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.total_quantity >= instance.sales_quantity:
            instance.total_quantity -= instance.sales_quantity
            instance.sales_created_by = str(request.user)
            messages.success(request, "Successfully sold " + str(instance.sales_quantity) + " " + str(instance.product_unit) + "s of " + str(instance.name) + '.    ' + str(instance.total_quantity) + " " +  str(instance.product_unit) + "s of " + str(instance.name) + " left on stock." )
            instance.save()
            #return redirect('/system/stock'+str(instance.id))
            return redirect('/system/stock')
        else:
            messages.error(request, "There is not enough products on stock")
    # else:
    #     messages.error(request, "Product or customer not active." )

    context = { 'product'  : product,
               'customers' : customers, 
                'form'     : form,
                'title'    : 'Issue ' + str(product.name),
                'username' : 'Sold By: ' + str(request.user)}
    return render(request, "system/product_sales.html", context)




# Product Purchase - 11th trial
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1'])
def product_purchase(request, pk):
    product   = Product.objects.get(id=pk)
    suppliers = Supplier.objects.all()
    form      = PurchaseForm(request.POST or None, instance=product)
    
    #if product.status=="Active" and customers.status=="Active":
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.total_quantity >= instance.purchase_quantity:
            instance.total_quantity += instance.purchase_quantity
            instance.purchase_created_by = str(request.user)
            messages.success(request, "Successfully purchased " + str(instance.purchase_quantity) + " " + str(instance.product_unit) + " of " + str(instance.name) + '.    ' + str(instance.total_quantity) + " " +  str(instance.product_unit) + "s of " + str(instance.name) + " now on stock." )
            instance.save()
            #return redirect('/system/stock'+str(instance.id))
            return redirect('/system/stock')
        else:
            messages.error(request, "There is not enough products on stock")
    # else:
    #     messages.error(request, "Product or customer not active." )

    context = { 'product'   : product,
                'suppliers' : suppliers, 
                'form'      : form,
                'title'     : 'Purchase ' + str(product.name),
                'username'  : 'Purchased By: ' + str(request.user)}
    return render(request, "system/product_purchase.html", context)


# ---------------------------------------------------------------------------------------------------------------
# Products List
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def product_list(request):

    #Search Bar
    if request.method == "POST":
        searched = request.POST['searched']
        product_list = Product.objects.filter(name__icontains=searched)
        
        # Pagination
        pag        = Paginator(product_list, 5)
        page       = request.GET.get('page')
        page_items = pag.get_page(page)
            
        context = { 'product_list' : product_list,
                    'page_items'   : page_items,
                    'searched'     : searched}
        return render(request, 'system/product_list.html', context)
    else:
        product_list = Product.objects.all()
        
        # Pagination
        pag        = Paginator(product_list, 5)
        page       = request.GET.get('page')
        page_items = pag.get_page(page)
            
        context = { 'product_list' : product_list,
                    'page_items'   : page_items}
        return render(request, 'system/product_list.html', context)

# Export Products List into CSV
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def product_list_csv(request):
    response                        = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="product_list.csv"'
    writer                          = csv.writer(response)
    product_list                    = Product.objects.all()

    writer.writerow( [ 'Product Code', 'Product Name', 'Category', 'Brand', 'Total Qty', 'Product Unit', 'Stock Alert Qty', 'Status', 'Description', 'Date created' ] )

    for product in product_list:
        writer.writerow( [ product.code, product.name, product.category, product.brand, product.product_price, product.total_quantity, product.stock_alert, product.status, product.description, product.date_created ] )
    
    return response
    

# Create Product
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1'])
def create_product(request, ):
    form = ProductForm()
    if request.method == 'POST':
        name  = request.POST['name']
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product - {name} - is Added')
            return redirect('/system/product_list')
        # else:
        #     messages.error(request, 'Problem processing your request')
        #     return redirect('/system/product_list')
    
    context = {'form' : form}
    return render(request, 'system/create_product.html', context)


# Update Product
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1'])
def update_product(request, pk):   
    product = Product.objects.get(id=pk)   
    form = ProductForm(instance=product)
    if request.method == 'POST':
        name  = request.POST['name']
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product - {name} - is Updated')
            return redirect('/system/product_list')
    
    context = {'form' : form}
    return render(request, 'system/create_product.html', context)

        
# Delete Product
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1'])
def delete_product(request, pk):    
    product = Product.objects.get(id=pk)   
    if request.method == "POST":
        product.delete()
        messages.success(request, f'Product {product.name} is Deleted')
        return redirect('/system/product_list')
    
    context = {'item' : product}
    return render(request, 'system/delete_product.html', context)


# Single Product Page View
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def single_product(request, pk):
    product_details = Product.objects.filter(id=pk)
    
    context = {'product_details' : product_details}
    return render(request, 'system/single_product.html', context)


# ---------------------------------------------------------------------------------------------------------------
# Customers List
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def customer_list(request):
    customer_list  = Customer.objects.all()
    
    #Search Bar
    if request.method == "POST":
        searched      = request.POST['searched']
        customer_list = Customer.objects.filter(name__icontains=searched)
    
        # Pagination
        pag        = Paginator(customer_list, 5)
        page       = request.GET.get('page')
        page_items = pag.get_page(page)
        
        context = {'customer_list' : customer_list,
                    'page_items'   : page_items}
        return render(request, 'system/customer_list.html', context)
    else:
        customer_list  = Customer.objects.all()
        
        # Pagination
        pag        = Paginator(customer_list, 5)
        page       = request.GET.get('page')
        page_items = pag.get_page(page)
        
        context = {'customer_list' : customer_list,
                    'page_items'   : page_items}
        return render(request, 'system/customer_list.html', context)

# Export Customer List into CSV
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def customer_list_csv(request):
    response                        = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customer_list.csv"'
    writer                          = csv.writer(response)
    customer_list                   = Customer.objects.all()

    writer.writerow( [ 'Customer Code', 'Customer Name', 'Phone', 'E-mail address', 'Country', 'City', 'Address', 'Status', 'Note', 'Date created' ] )

    for customer in customer_list:
        writer.writerow( [ customer.code, customer.name, customer.phone, customer.email, customer.country, customer.city, customer.address, customer.status, customer.description, customer.date_created ] )
    
    return response
    

# Create Customer
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1'])
def create_customer(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            name = request.POST['name']
            form.save()
            messages.success(request, f'Customer {name} Added')
            return redirect('/system/customer_list')
        # else:
        #     messages.error(request, 'Problem processing your request')
        #     return redirect('/system/customer_list')
        
    context = {'form' : form}
    return render(request, 'system/create_customer.html', context)


# Update Customer
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1'])
def update_customer(request, pk):   
    customer = Customer.objects.get(id=pk)   
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            name = request.POST['name']
            form.save()
            messages.success(request, f'Customer {name} is Updated')
            return redirect('/system/customer_list')
    
    context = {'form' : form}
    return render(request, 'system/create_customer.html', context)

# Delete Customer
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1'])
def delete_customer(request, pk):    
    customer = Customer.objects.get(id=pk)   
    if request.method == "POST":
        customer.delete()
        #messages.success(request, 'Customer Sucessfully Deleted')
        messages.success(request, f'Customer {customer.name} Sucessfully Deleted')
        return redirect('/system/customer_list')
    
    context = {'item' : customer}
    return render(request, 'system/delete_customer.html', context)


# Single Customer Page View
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def single_customer(request, pk):
    customer_details = Customer.objects.filter(id=pk)
    
    context = { 'customer_details'  : customer_details }
    return render(request, 'system/single_customer.html', context)

# Single Customer Report
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def customer_report(request, pk):
    customer_sales = Customer.objects.get(id=pk)
    products       = Product.objects.filter(customer=customer_sales)
    
    # Pagination
    pag        = Paginator(products, 5)
    page       = request.GET.get('page')
    page_items = pag.get_page(page)
        
    context = { 'customer_sales'   : customer_sales,
                'page_items'       : page_items}
    return render(request, 'system/customer_report.html', context)

# ---------------------------------------------------------------------------------------------------------------

# Supplier List
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def supplier_list(request):
    supplier_list = Supplier.objects.all()
    
    #Search Bar
    if request.method == "POST":
        searched      = request.POST['searched']
        supplier_list = Supplier.objects.filter(name__icontains=searched)
    
        # Pagination
        pag        = Paginator(supplier_list, 5)
        page       = request.GET.get('page')
        page_items = pag.get_page(page)
        
        context = {'supplier_list' : supplier_list,
                    'page_items'   : page_items}
        
        return render(request, 'system/supplier_list.html', context)
    else:
        supplier_list = Supplier.objects.all()
        
        # Pagination
        pag        = Paginator(supplier_list, 5)
        page       = request.GET.get('page')
        page_items = pag.get_page(page)
        
        context = {'supplier_list' : supplier_list,
                    'page_items'   : page_items}
        
    return render(request, 'system/supplier_list.html', context)

# Export Supplier List into CSV
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def supplier_list_csv(request):
    response                        = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="supplier_list.csv"'
    writer                          = csv.writer(response)
    supplier_list                   = Supplier.objects.all()

    writer.writerow( [ 'Supplier Code', 'Supplier Name', 'Phone', 'E-mail address', 'Country', 'City', 'Address', 'Status', 'Note', 'Date created' ] )

    for supplier in supplier_list:
        writer.writerow( [ supplier.code, supplier.name, supplier.phone, supplier.email, supplier.country, supplier.city, supplier.address, supplier.status, supplier.description, supplier.date_created ] )
    
    return response
    

# Create Supplier
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1'])
def create_supplier(request):
    form = SupplierForm()
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            name = request.POST['name']
            form.save()
            messages.success(request, f'Supplier - {name} - Added')
            return redirect('/system/supplier_list')
        # else:
        #     messages.error(request, 'Problem processing your request')
        #     return redirect('/system/supplier_list')
        
    context = {'form' : form}   
    return render(request, 'system/create_Supplier.html', context)


# Update Supplier
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1'])
def update_supplier(request, pk): 
    supplier = Supplier.objects.get(id=pk)   
    form = SupplierForm(instance=supplier)
    if request.method == 'POST':
        name = request.POST['name']
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, f'Supplier - {name} - Updated')
            return redirect('/system/supplier_list')
    
    context = {'form' : form}
    return render(request, 'system/create_supplier.html', context)

# Delete Supplier
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1'])
def delete_supplier(request, pk): 
    supplier = Supplier.objects.get(id=pk)   
    if request.method == "POST":
        supplier.delete()
        messages.success(request, f'Supplier - {supplier.name} - Sucessfully Deleted')
        return redirect('/system/supplier_list')
    
    context = {'item' : supplier}
    return render(request, 'system/delete_supplier.html', context)


# Single Supplier Page View
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def single_supplier(request, pk):
    supplier_details = Supplier.objects.filter(id=pk)
    
    context = { 'supplier_details'  : supplier_details }
    return render(request, 'system/single_supplier.html', context)


# Single Supplier Report
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def supplier_report(request, pk):
    supplier_purchase = Supplier.objects.get(id=pk)
    products          = Product.objects.filter(supplier=supplier_purchase)
    
    # Pagination
    pag        = Paginator(products, 5)
    page       = request.GET.get('page')
    page_items = pag.get_page(page)
    
    context = { 'supplier_purchase' : supplier_purchase,
                'page_items'        : page_items}
    return render(request, 'system/supplier_report.html', context)

#  ---------------------------------------------------------------------------------------------------------------

# Category List
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def category_list(request):
    category_list = Category.objects.all()
    
    #Search Bar
    if request.method == "POST":
        searched = request.POST['searched']
        category_list = Category.objects.filter(name__icontains=searched)
    
        # Pagination
        pag        = Paginator(category_list, 5)
        page       = request.GET.get('page')
        page_items = pag.get_page(page)
        
        context = { 'category_list' : category_list,
                    'page_items'   : page_items}
        return render(request, 'system/category_list.html', context)
    else:
        category_list = Category.objects.all()
        
        # Pagination
        pag        = Paginator(category_list, 5)
        page       = request.GET.get('page')
        page_items = pag.get_page(page)
        
        context = { 'category_list' : category_list,
                    'page_items'   : page_items}
        return render(request, 'system/category_list.html', context)

# Export Category List into CSV
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def category_list_csv(request):
    response                        = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="category_list.csv"'
    writer                          = csv.writer(response)
    category_list                   = Category.objects.all()

    writer.writerow( [ 'Category Code', 'Category Name', 'Note', 'Date created' ] )

    for category in category_list:
        writer.writerow( [ category.code, category.name, category.description, category.date_created ] )
    
    return response

# Create Category
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1'])
def create_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        name = request.POST['name']
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category - {name} - Added')
            return redirect('/system/category_list')
        # else:
        #     messages.error(request, 'Problem processing your request')
        #     return redirect('/system/category_list')
        
    context = {'form' : form}   
    return render(request, 'system/create_category.html', context)


# Update Category
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1'])
def update_category(request, pk):
    category = Category.objects.get(id=pk)   
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        name = request.POST['name']
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category - {name} - Updated')
            return redirect('/system/category_list')
    
    context = {'form' : form}
    return render(request, 'system/create_category.html', context)

# Delete Category
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1'])
def delete_category(request, pk): 
    category = Category.objects.get(id=pk)   
    if request.method == "POST":
        category.delete()
        messages.success(request, f'Category - {category.name} - Sucessfully Deleted')
        return redirect('/system/category_list')
    
    context = {'item' : category}
    return render(request, 'system/delete_category.html', context)

# ---------------------------------------------------------------------------------------------------------------

# Brand List
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def brand_list(request):
    brand_list  = Brand.objects.all()
    
    #Search Bar
    if request.method == "POST":
        searched = request.POST['searched']
        brand_list = Brand.objects.filter(name__icontains=searched)
        
        # Pagination
        pag        = Paginator(brand_list, 5)
        page       = request.GET.get('page')
        page_items = pag.get_page(page)
        
        context = { 'brand_list' : brand_list,
                    'page_items'   : page_items}
        return render(request, 'system/brand_list.html', context)
    else:
        brand_list  = Brand.objects.all()
        
        # Pagination
        pag        = Paginator(brand_list, 5)
        page       = request.GET.get('page')
        page_items = pag.get_page(page)
        
        context = { 'brand_list' : brand_list,
                    'page_items'   : page_items}
        return render(request, 'system/brand_list.html', context)

# Export Brand List into CSV
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def brand_list_csv(request):
    response                        = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="brand_list.csv"'
    writer                          = csv.writer(response)
    brand_list                      = Brand.objects.all()

    writer.writerow( [ 'Brand Code', 'Brand Name', 'Note', 'Date created' ] )

    for brand in brand_list:
        writer.writerow( [ brand.code, brand.name, brand.description, brand.date_created ] )
    
    return response

# Create Brand
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1'])
def create_brand(request):
    form = BrandForm()
    if request.method == 'POST':
        name  = request.POST['name']
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # messages.success(request, f'New Brand Added')
            messages.success(request, f'Brand - {name} - Added')
            return redirect('/system/brand_list')
        # else:
        #     messages.error(request, 'Problem processing your request')
        #     return redirect('/system/brand_list')
        
    context = {'form' : form}
    return render(request, 'system/create_brand.html', context)


# Update Brand
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1'])
def update_brand(request, pk):   
    brand = Brand.objects.get(id=pk)   
    form = BrandForm(instance=brand)
    if request.method == 'POST':
        name = request.POST['name']
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            messages.success(request, f'Brand - {name} - Updated')
            return redirect('/system/brand_list')
    
    context = {'form' : form}
    return render(request, 'system/create_brand.html', context)

# Delete Brand
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1'])
def delete_brand(request, pk):    
    brand = Brand.objects.get(id=pk)   
    if request.method == "POST":
        brand.delete()
        messages.success(request, f'Brand - {brand.name} - Sucessfully Deleted')
        return redirect('/system/brand_list')
    
    context = {'item' : brand}
    return render(request, 'system/delete_brand.html', context)

# ---------------------------------------------------------------------------------------------------------------

# Unit List
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def units_list(request):
    units_list = Unit.objects.all() 
    
     #Search Bar
    if request.method == "POST":
        searched   = request.POST['searched']
        units_list = Unit.objects.filter(name__icontains=searched)
        
        # Pagination
        pag        = Paginator(units_list, 5)
        page       = request.GET.get('page')
        page_items = pag.get_page(page)
        
        context = { 'units_list' : units_list,
                    'page_items'   : page_items}
        return render(request, 'system/units_list.html', context)
    else:
        units_list = Unit.objects.all() 
        
        # Pagination
        pag        = Paginator(units_list, 5)
        page       = request.GET.get('page')
        page_items = pag.get_page(page)
        
        context = { 'units_list' : units_list,
                    'page_items'   : page_items}
        return render(request, 'system/units_list.html', context)
    

# Export Unit List into CSV
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def unit_list_csv(request):
    response                        = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="unit_list.csv"'
    writer                          = csv.writer(response)
    unit_list                       = Unit.objects.all()

    writer.writerow( [ 'Unit Code', 'Unit Name', 'Unit Abbreviation' 'Note', 'Date created' ] )

    for unit in unit_list:
        writer.writerow( [ unit.code, unit.name, unit.unit_abbreviation, unit.description, unit.date_created ] )
    
    return response

# Create Unit
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1'])
def create_unit(request):
    form = UnitForm()
    if request.method == 'POST':
        name = request.POST['name']
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Unit - {name} - Added')
            return redirect('/system/units_list')
        # else:
        #     messages.error(request, 'Problem processing your request')
        #     return redirect('/system/units_list')
        
    context = {'form' : form}
    return render(request, 'system/create_unit.html', context)


# Update Unit
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1'])
def update_unit(request, pk):   
    unit = Unit.objects.get(id=pk)   
    form = UnitForm(instance=unit)
    if request.method == 'POST':
        name = request.POST['name']
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            messages.success(request, f'Unit - {name} - Updated')
            return redirect('/system/units_list')
    
    context = {'form' : form}
    return render(request, 'system/create_unit.html', context)

# Delete Unit
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1'])
def delete_unit(request, pk):    
    unit = Unit.objects.get(id=pk)   
    if request.method == "POST":
        unit.delete()
        messages.success(request, f'Unit - {unit.name} - Sucessfully Deleted')
        return redirect('/system/units_list')
    
    context = {'item' : unit}
    return render(request, 'system/delete_unit.html', context)

# ---------------------------------------------------------------------------------------------------------------

# Report Payment Sales
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def report_payment_sales(request):
    return render(request, 'system/report_payment_sales.html')

# Report Payment Sales Returns
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def report_payment_sales_returns(request):
    return render(request, 'system/report_payment_sales_returns.html')

# Report Payment Purchases
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def report_payment_purchases(request):
    return render(request, 'system/report_payment_purchases.html')

# Report Payment Purchases Returns
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def report_payment_purchases_returns(request):
    return render(request, 'system/report_payment_purchases_returns.html')


# ---------------------------------------------------------------------------------------------------------------
# Report Product Quantity Alert
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def report_product_quantity_alert(request):
    all_products = Product.objects.all()
    
    #Search Bar
    if request.method == "POST":
        searched = request.POST['searched']
        all_products = Product.objects.filter(name__icontains=searched)

    # Pagination
    pag        = Paginator(all_products, 20)
    page       = request.GET.get('page')
    page_items = pag.get_page(page)
    
    context = { 'all_products' : all_products,
                'page_items'   : page_items}    
    return render(request, 'system/report_product_quantity_alert.html', context)


# Export Stock Alert List into CSV
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def stock_alert_list_csv(request):
    response                        = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stock_alert_list.csv"'
    writer                          = csv.writer(response)
    #product                         = Product.objects.all()
    #product_list                    = Product.objects.filter(product.total_quantity <= product.stock_alert)
    product_list                     = Product.objects.all()

    writer.writerow( [ 'Product Code', 'Product Name', 'Total Qty', 'Product Unit', 'Stock Alert Qty' ] )

    for product in product_list:
        writer.writerow( [ product.code, product.name, product.total_quantity, product.product_unit, product.stock_alert ] )
    
    return response
    


# Report Top Selling Products
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def report_top_selling_products(request):
    return render(request, 'system/report_top_selling_products.html')


# Report Customer Purchases
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def report_customer_purchases(request):
    return render(request, 'system/customer_purchases.html')


# Report Best Customers
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def report_best_customers(request):
    products = Product.objects.all()
    orders   = products.customer_set.all()
    print("ovo su orderi", orders)
    
    context = {'orders' : orders}
    return render(request, 'system/report_best_customers.html', context)

# ---------------------------------------------------------------------------------------------------------------

















# ---------------------------------------------------------------------------------------------------------------
### !!! COMING SOON !!! ###

# ---------------------------------------------------------------------------------------------------------------

# Warehouse Adjustments - Adding Products to Warehouse
#@login_required(login_url='login_page')
"""def adjustment_add(request, pk):
    form    = AdjustmentAddForm()
    if request.method == 'POST':
        form = AdjustmentAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/system/product_list')
        else:
            print(form.errors.as_data())
  
    context = {'form' : form}
    return render(request, 'system/warehouse_adjustments_adding.html', context)"""
    
"""def adjustment_add(request, pk):
    AdjustmentAddFormSet = inlineformset_factory(Product, AdjustmentAdd, fields=('product', 'quantity')) #umjesto adjustmentadd mozda warehouse model
    product              = Product.objects.get(id=pk)
    formset              = AdjustmentAddFormSet(instance=product)
    #form                 = AdjustmentAddForm(initial={'product' : product})
    if request.method == "POST":
        form = AdjustmentAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/system/product_list')
        
    context = {'formset' : formset}
    return render(request, 'system/warehouse_adjustments_adding.html', context)"""
    
"""def adjustment_add(request, pk):
    product = Product.objects.get(id=pk)
    products = Product.objects.all()
    adjustment_add = AdjustmentAdd.objects.all()
    form    = AdjustmentAddForm(initial={'product' : product})
    #total_quantity = Product.objects.raw("SELECT total_quantity FROM system_product")
    

    if request.method == "POST":
        # if product.total_quantity >= adjustment_add.quantity:
        form = AdjustmentAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/system/product_list')
            # else:
            #     return redirect('/system/dashboard')
                
    
    context = {'form' : form}
    return render(request, 'system/warehouse_adjustments_adding.html', context)"""
    
    
"""def adjustment_add(request, pk):
    product = Product.objects.get(id=pk)
    products = Product.objects.all()
    adjustment_add = AdjustmentAdd.objects.all()
    form    = AdjustmentAddForm(initial={'product' : product})
    #total_quantity = Product.objects.raw("SELECT total_quantity FROM system_product")
    #total_quantity = Product.objects.filter()
    
    print(product.total_quantity)
    
    # print("TOTAL QUANTITY FROM PRODUCT MODEL", total_quantity)
    # print("QS all products", products)

    if request.method == "POST":
        #if product.total_quantity >= adjustment_add.quantity:
        form = AdjustmentAddForm(request.POST)
        print(request.POST, "ovo je post")
        if form.is_valid():
            form.save()
            return redirect('/system/product_list')
            else:
                return redirect('/system/dashboard')
    
                
    
    context = {'form' : form}
    return render(request, 'system/warehouse_adjustments_adding.html', context)"""

#@login_required(login_url='login_page')
"""def adjustment_add(request, pk):
    product = Product.objects.get(id=pk)
    warehouse = Warehouse.objects.get(name=request.POST.get("warehouse"))
    quantity  = request.POST.get("quantity")
    adjustment_add = AdjustmentAdd(quantity=quantity, product=product, warehouse=warehouse)
    adjustment_add.save()
    
    context = {'adjustment_add' : adjustment_add,
               'quantity' : 'quantity',
               'product' : 'product',
               'warehouse' : 'warehouse'}
    return render(request, 'system/warehouse_adjustments_adding.html', context)"""



# WORK ON Quantity on Stock Per Warehouse
#@login_required(login_url='login_page')


# ---------------------------------------------------------------------------------------------------------------

# Expense Category
#@login_required(login_url='login_page')
"""def expense_category_list(request):
    expense_category_list = Expense_Category.objects.all()
    
    # Pagination
    pag        = Paginator(expense_category_list, 2)
    page       = request.GET.get('page')
    page_items = pag.get_page(page)
    
    context = { 'expense_category_list' : expense_category_list,
                'page_items'            : page_items}
    return render(request, 'system/expense_category_list.html', context)"""

#@login_required(login_url='login_page')
"""def create_expense_category(request):
    form = Expense_CategoryForm()
    if request.method == 'POST':
        form = Expense_CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/system/expense_category_list')
        
    context = {'form' : form}
    return render(request, 'system/create_expense_category.html', context)"""

# Update Expense Category
#@login_required(login_url='login_page')
"""def update_expense_category(request, pk):   
    expense_category = Expense_Category.objects.get(id=pk)   
    form = Expense_CategoryForm(instance=expense_category)
    if request.method == 'POST':
        form = Expense_CategoryForm(request.POST, instance=expense_category)
        if form.is_valid():
            form.save()
            return redirect('/system/expense_category_list')
    
    context = {'form' : form}
    return render(request, 'system/create_expense_category.html', context)"""

# Delete Expense Category
#@login_required(login_url='login_page')
"""def delete_expense_category(request, pk):    
    expense_category = Expense_Category.objects.get(id=pk)   
    if request.method == "POST":
        expense_category.delete()
        return redirect('/system/expense_category_list')
    
    context = {'item' : expense_category}
    return render(request, 'system/delete_expense_category.html', context)"""


# ---------------------------------------------------------------------------------------------------------------

# Sales List
#@login_required(login_url='login_page')
"""def sales_list(request):
    sale_list = Sale.objects.all()
    
    # Pagination
    pag        = Paginator(sale_list, 2)
    page       = request.GET.get('page')
    page_items = pag.get_page(page)
    
    context = { 'sale_list'  : sale_list,
                'page_items' : page_items}
    return render(request, 'system/sales_list.html', context)"""


# Create Sales
#@login_required(login_url='login_page')
"""def create_sales(request):
    return render(request, 'system/create_sales.html')"""

# ---------------------------------------------------------------------------------------------------------------

# Purchase List
#@login_required(login_url='login_page')
"""def purchase_list(request):
    #purchases_list = Purchase.objects.all()
    
    # Pagination
    pag        = Paginator(purchases_list, 2)
    page       = request.GET.get('page')
    page_items = pag.get_page(page)
    
    context = { 'purchases_list'  : purchases_list,
                'page_items'      : page_items}
    return render(request, 'system/sales_list.html', context)
    return render(request, 'system/purchase_list.html')"""

# Create Purchase
#@login_required(login_url='login_page')
"""def create_purchase(request):
    return render(request, 'system/create_purchase.html')"""

# ---------------------------------------------------------------------------------------------------------------

# Sales Return List
#@login_required(login_url='login_page')
"""def sales_return_list(request):
     #sale_return_list = SaleReturns.objects.all()
    
    # Pagination
    pag        = Paginator(sale_return_list, 2)
    page       = request.GET.get('page')
    page_items = pag.get_page(page)
    
    context = { 'sale_return_list'  : sale_return_list,
                'page_items'        : page_items}
    return render(request, 'system/sales_list.html', context) 
    return render(request, 'system/sales_return_list.html')"""

# Create Sales Return
#@login_required(login_url='login_page')
"""def create_sales_return(request):
    return render(request, 'system/create_sales_return.html')"""

# ---------------------------------------------------------------------------------------------------------------

# Purchase Return List
#@login_required(login_url='login_page')
"""def purchase_return_list(request):
     #purchase_return_list = PurchaseReturns.objects.all()
    
    # Pagination
    pag        = Paginator(purchase_return_list, 2)
    page       = request.GET.get('page')
    page_items = pag.get_page(page)
    
    context = { 'purchase_return_list'  : purchase_return_list,
                'page_items'            : page_items}
    return render(request, 'system/sales_list.html', context)
    return render(request, 'system/purchase_return_list.html')"""

# Create Purchase Return
#@login_required(login_url='login_page')
"""def create_purchase_return(request):
    return render(request, 'system/create_purchase_return.html')"""

# ---------------------------------------------------------------------------------------------------------------

# Expense List
#@login_required(login_url='login_page')
"""def expsense_list(request):
     #expense_list = Expense.objects.all()
    
    # Pagination
    pag        = Paginator(expense_list, 2)
    page       = request.GET.get('page')
    page_items = pag.get_page(page)
    
    context = { 'expense_list' : expense_list,
                'page_items'   : page_items}
    return render(request, 'system/sales_list.html', context)  
    return render(request, 'system/expenses_list.html')"""

# Create Expense
#@login_required(login_url='login_page')
"""def create_expense(request):
    return render(request, 'system/create_expense.html')"""


# ---------------------------------------------------------------------------------------------------------------

# Warehouse List
#@login_required(login_url='login_page')
"""def warehouse_list(request):
    warehouse_list = Warehouse.objects.all()
    
    # Pagination
    pag        = Paginator(warehouse_list, 2)
    page       = request.GET.get('page')
    page_items = pag.get_page(page)
    
    context = {'warehouse_list' : warehouse_list,
                'page_items'   : page_items}
    return render(request, 'system/warehouse_list.html', context)"""

# Create Warehouse
#@login_required(login_url='login_page')
"""def create_warehouse(request):
    form = WarehouseForm()
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/system/warehouse_list')
        
    context = {'form' : form}   
    return render(request, 'system/create_warehouse.html', context)"""

# Update Warehouse
#@login_required(login_url='login_page')
"""def update_warehouse(request, pk): 
    warehouse = Warehouse.objects.get(id=pk)   
    form = WarehouseForm(instance=warehouse)
    if request.method == 'POST':
        form = WarehouseForm(request.POST, instance=warehouse)
        if form.is_valid():
            form.save()
            return redirect('/system/warehouse_list')
    
    context = {'form' : form}
    return render(request, 'system/create_warehouse.html', context)"""

# Delete Warehouse
#@login_required(login_url='login_page')
"""def delete_warehouse(request, pk): 
    warehouse = Warehouse.objects.get(id=pk)   
    if request.method == "POST":
        warehouse.delete()
        return redirect('/system/warehouse_list')
    
    context = {'item' : warehouse}
    return render(request, 'system/delete_warehouse.html', context)"""


# Single Warehouse Page View
#@login_required(login_url='login_page')
"""def single_warehouse(request, pk):
    single_warehouse = Warehouse.objects.filter(id=pk)
    
    context = {'single_warehouse' : single_warehouse}
    return render(request, 'system/single_warehouse.html', context)"""
    
    
    # Graphs
"""@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def ggtopcustomers(request): #zing chart - chart_sales_data
    
    # customer = Customer.objects.get(id=pk)
    # products_per_customer = customer.product_set.all()
    
    customer = Customer.objects.all()
    products = Product.objects.all().filter(sales_quantity = 1)
    
    #relatedset = customer.product_set.all()
    
    print("Customers: ", customer)
    print("Products: ", products)
    #print("relatedset: ", relatedset)
    
    context = {'customer' : customer,
               'products' : products}
    return render(request, 'system/report_best_customer.html', context)"""


"""@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Administrator', 'Manager', 'Staff - Level 1', 'Staff - Level 2'])
def topcustomers(request):
    customer = Customer.objects.all()
    products       = Product.objects.all()
    

    sales = Customer.objects.filter(pk__in=products.values('customer_id')).exclude(name="Walk-in customer")
    
    sales = customer.product_set.all()
    
    for sale in sales:
        print("ovo je order: ", sale)
    
    context = { 'customer' : customer,
                'products'       : products,
                'sales' : sales}
    return render(request, 'system/report_best_customer.html', context)"""