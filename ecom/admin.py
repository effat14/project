from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .models import *


class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name'
    )
    search_fields = (
        'id',
        'name'
    )


admin.site.register(Company, CompanyAdmin)


class CustomAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'profile_pic',
        'address',
        'mobile',
        'created_at'
    )
    search_fields = (
        'id',
        'user',
        'profile_pic',
        'address',
        'mobile',
        'created_at'
    )


admin.site.register(Customer, CustomAdmin)


class MedicineAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'company',
        'name',
        'product_image',
        'description',
        'cost',
        'selling_price',
        'qty',
        'created_at'
    )
    search_fields = (
        'id',
        'company',
        'name',
        'product_image',
        'description',
        'cost',
        'selling_price',
        'qty',
        'created_at'
    )


admin.site.register(Medicine, MedicineAdmin)


class OrdersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'email',
        'address',
        'mobile',
        'total_price',
        'order_date',
        'status',
        'created_at'
    )
    search_fields = (
        'id',
        'user',
        'email',
        'address',
        'mobile',
        'total_price',
        'order_date',
        'status',
        'created_at'
    )
    list_filter = ['status']


admin.site.register(Orders, OrdersAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'medicine',
        'created_at',
        'updated_at',
        'price',
        'quantity'
    )
    search_fields = (
        'id',
        'order',
        'medicine',
        'created_at',
        'updated_at',
        'price',
        'quantity'
    )


admin.site.register(OrderItem, OrderItemAdmin)
