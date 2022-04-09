from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main.models import CustomUser, Product, OrderItem, Order, General_Product, ProductFB, Category
from django.contrib.auth import get_user_model
User = get_user_model()

class CustomUserAdmin(UserAdmin):
    pass

admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(General_Product)
admin.site.register(CustomUser)
admin.site.register(ProductFB)
admin.site.register(Category)