from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Expense_Category)
admin.site.register(Unit)
admin.site.register(Warehouse)

