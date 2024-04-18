from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Customer)
admin.site.register(Medicine)
admin.site.register(Orders)
admin.site.register(OrderItem)
