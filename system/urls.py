from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register_page/', views.register_page, name="register_page"),
    path('login_page/', views.login_page, name="login_page"),
    path('logout_user/', views.logout_user, name="logout_user"),
    
    
    path('dashboard/', views.dashboard, name="dashboard"),
    
    
    path('product_list/', views.product_list, name="product_list"),
    path('create_product/', views.create_product, name="create_product"),
    
    path('customer_list/', views.customer_list, name="customer_list"),
    path('create_customer/', views.create_customer, name="create_customer"),
    path('update_customer/<str:pk>/', views.update_customer, name="update_customer"),
    path('delete_customer/<str:pk>/', views.delete_customer, name="delete_customer"),
    
    
    path('supplier_list/', views.supplier_list, name="supplier_list"),
    path('create_supplier/', views.create_supplier, name="create_supplier"),
    path('update_supplier/<str:pk>/', views.update_supplier, name="update_supplier"),
    path('delete_supplier/<str:pk>/', views.delete_supplier, name="delete_supplier"),
    
    path('warehouse_list/', views.warehouse_list, name="warehouse_list"),
    path('create_warehouse/', views.create_warehouse, name="create_warehouse"),
    path('update_warehouse/<str:pk>/', views.update_warehouse, name="update_warehouse"),
    path('delete_warehouse/<str:pk>/', views.delete_warehouse, name="delete_warehouse"),

    
    path('category_list/', views.category_list, name="category_list"),
    path('create_category/', views.create_category, name="create_category"),
    path('update_category/<str:pk>/', views.update_category, name="update_category"),
    path('delete_category/<str:pk>/', views.delete_category, name="delete_category"),
    
    path('brand_list/', views.brand_list, name="brand_list"),
    path('create_brand/', views.create_brand, name="create_brand"),
    path('update_brand/<str:pk>/', views.update_brand, name="update_brand"),
    path('delete_brand/<str:pk>/', views.delete_brand, name="delete_brand"),
           
    path('units_list/', views.units_list, name="units_list"),
    path('create_unit/', views.create_unit, name="create_unit"),
    path('update_unit/<str:pk>/', views.update_unit, name="update_unit"),
    path('delete_unit/<str:pk>/', views.delete_unit, name="delete_unit"),
    
    
    path('expsense_list/', views.expsense_list, name="expsense_list"),
    path('create_expense/', views.create_expense, name="create_expense"),
    
    path('expense_category_list/', views.expense_category_list, name="expense_category_list"),
    path('create_expense_category/', views.create_expense_category, name="create_expense_category"),
    path('update_expense_category/<str:pk>/', views.update_expense_category, name="update_expense_category"),
    path('delete_expense_category/<str:pk>/', views.delete_expense_category, name="delete_expense_category"),
    
    
    
    path('sales_list/', views.sales_list, name="sales_list"),
    path('create_sales/', views.create_sales, name="create_sales"),
    
    path('purchase_list/', views.purchase_list, name="purchase_list"),
    path('create_purchase/', views.create_purchase, name="create_purchase"),
    
    path('sales_return_list/', views.sales_return_list, name="sales_return_list"),
    path('create_sales_return/', views.create_sales_return, name="create_sales_return"),
    
    path('purchase_return_list/', views.purchase_return_list, name="purchase_return_list"),
    path('create_purchase_return/', views.create_purchase_return, name="create_purchase_return"),
    
    
    path('report_payment_sales/', views.report_payment_sales, name="report_payment_sales"),
    path('report_payment_sales_returns/', views.report_payment_sales_returns, name="report_payment_sales_returns"),
    path('report_payment_purchases/', views.report_payment_purchases, name="report_payment_purchases"),
    path('report_payment_purchases_returns/', views.report_payment_purchases_returns, name="report_payment_purchases_returns"),
    path('report_product_quantity_alert/', views.report_product_quantity_alert, name="report_product_quantity_alert"),
    path('report_top_selling_products/', views.report_top_selling_products, name="report_top_selling_products"),
    path('report_best_customers/', views.report_best_customers, name="report_best_customers"),


]
