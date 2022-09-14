from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.conf import settings
from django.conf.urls.static import static
from .forms import UserPasswordResetForm
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    
    path('register_page/', views.register_page, name="register_page"),
    path('login_page/', views.login_page, name="login_page"),
    path('logout_user/', views.logout_user, name="logout_user"),
    
    path('users_list/', views.users_list, name="users_list"),
    path('users_list_csv/', views.users_list_csv, name="users_list_csv"),
    path('user_page/', views.user_page, name="user_page"),  
    path('user_settings/', views.user_settings, name="user_settings"),  
           
    # path('password_reset/', PasswordResetView.as_view(template_name="system/password_reset.html"), name="reset_password"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='system/password_reset.html',
    form_class=UserPasswordResetForm), name='reset_password'),
    path('password_reset_sent/', PasswordResetDoneView.as_view(template_name="system/password_reset_sent.html"), name='password_reset_done'), 
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="system/password_reset_form.html"), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(template_name="system/password_reset_done.html"), name='password_reset_complete'),
    
    path('dashboard/', views.dashboard, name="dashboard"),  

    
    path('stock/', views.stock, name="stock"),  
    path('stock_list_csv/', views.stock_list_csv, name="stock_list_csv"),
    path('stock_detail/<str:pk>/', views.stock_detail, name="stock_detail"),
    path('product_sales/<str:pk>/', views.product_sales, name="product_sales"),
    path('product_purchase/<str:pk>/', views.product_purchase, name="product_purchase"),
    
    path('product_list/', views.product_list, name="product_list"),
    path('product_list_csv/', views.product_list_csv, name="product_list_csv"),
    path('create_product/', views.create_product, name="create_product"),
    path('update_product/<str:pk>/', views.update_product, name="update_product"),
    path('delete_product/<str:pk>/', views.delete_product, name="delete_product"),
    path('single_productt/<str:pk>/', views.single_product, name="single_product"),
    
    
    path('customer_list/', views.customer_list, name="customer_list"),
    path('customer_list_csv/', views.customer_list_csv, name="customer_list_csv"),
    path('create_customer/', views.create_customer, name="create_customer"),
    path('update_customer/<str:pk>/', views.update_customer, name="update_customer"),
    path('delete_customer/<str:pk>/', views.delete_customer, name="delete_customer"),
    path('single_customer/<str:pk>/', views.single_customer, name="single_customer"),
    path('customer_report/<str:pk>/', views.customer_report, name="customer_report"),
    
    
    path('supplier_list/', views.supplier_list, name="supplier_list"),
    path('supplier_list_csv/', views.supplier_list_csv, name="supplier_list_csv"),
    path('create_supplier/', views.create_supplier, name="create_supplier"),
    path('update_supplier/<str:pk>/', views.update_supplier, name="update_supplier"),
    path('delete_supplier/<str:pk>/', views.delete_supplier, name="delete_supplier"),
    path('single_supplier/<str:pk>/', views.single_supplier, name="single_supplier"),
    path('supplier_report/<str:pk>/', views.supplier_report, name="supplier_report"),
        
    
    path('category_list/', views.category_list, name="category_list"),
    path('category_list_csv/', views.category_list_csv, name="category_list_csv"),
    path('create_category/', views.create_category, name="create_category"),
    path('update_category/<str:pk>/', views.update_category, name="update_category"),
    path('delete_category/<str:pk>/', views.delete_category, name="delete_category"),
    
    path('brand_list/', views.brand_list, name="brand_list"),
    path('brand_list_csv/', views.brand_list_csv, name="brand_list_csv"),
    path('create_brand/', views.create_brand, name="create_brand"),
    path('update_brand/<str:pk>/', views.update_brand, name="update_brand"),
    path('delete_brand/<str:pk>/', views.delete_brand, name="delete_brand"),
           
    path('units_list/', views.units_list, name="units_list"),
    path('unit_list_csv/', views.unit_list_csv, name="unit_list_csv"),
    path('create_unit/', views.create_unit, name="create_unit"),
    path('update_unit/<str:pk>/', views.update_unit, name="update_unit"),
    path('delete_unit/<str:pk>/', views.delete_unit, name="delete_unit"),
    
    
    path('report_product_quantity_alert/', views.report_product_quantity_alert, name="report_product_quantity_alert"),
    path('stock_alert_list_csv/', views.stock_alert_list_csv, name="stock_alert_list_csv"),
    
    
    path('report_top_selling_products/', views.report_top_selling_products, name="report_top_selling_products"),
    path('report_customer_purchases/', views.report_customer_purchases, name="report_customer_purchases"),
    path('report_best_customers/', views.report_best_customers, name="report_best_customers"),
    
    
    
    
    
    
    # ---------------------------------------------------------------------------------------------------------------
    # !!! COMING SOON !!!
        
    # path('warehouse_list/', views.warehouse_list, name="warehouse_list"),
    # path('create_warehouse/', views.create_warehouse, name="create_warehouse"),
    # path('update_warehouse/<str:pk>/', views.update_warehouse, name="update_warehouse"),
    # path('delete_warehouse/<str:pk>/', views.delete_warehouse, name="delete_warehouse"),
    # path('single_warehouse/<str:pk>/', views.single_warehouse, name="single_warehouse"),

    #path('adjustment_add/<str:pk>/', views.adjustment_add, name="adjustment_add"),
    
    # path('expsense_list/', views.expsense_list, name="expsense_list"),
    # path('create_expense/', views.create_expense, name="create_expense"),
    
    # path('expense_category_list/', views.expense_category_list, name="expense_category_list"),
    # path('create_expense_category/', views.create_expense_category, name="create_expense_category"),
    # path('update_expense_category/<str:pk>/', views.update_expense_category, name="update_expense_category"),
    # path('delete_expense_category/<str:pk>/', views.delete_expense_category, name="delete_expense_category"),
    
    # path('sales_list/', views.sales_list, name="sales_list"),
    # path('create_sales/', views.create_sales, name="create_sales"),
    
    # path('purchase_list/', views.purchase_list, name="purchase_list"),
    # path('create_purchase/', views.create_purchase, name="create_purchase"),
    
    # path('sales_return_list/', views.sales_return_list, name="sales_return_list"),
    # path('create_sales_return/', views.create_sales_return, name="create_sales_return"),
    
    # path('purchase_return_list/', views.purchase_return_list, name="purchase_return_list"),
    # path('create_purchase_return/', views.create_purchase_return, name="create_purchase_return"),
    
    # path('report_payment_sales/', views.report_payment_sales, name="report_payment_sales"),
    # path('report_payment_sales_returns/', views.report_payment_sales_returns, name="report_payment_sales_returns"),
    # path('report_payment_purchases/', views.report_payment_purchases, name="report_payment_purchases"),
    # path('report_payment_purchases_returns/', views.report_payment_purchases_returns, name="report_payment_purchases_returns"),

]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)