from django.contrib import admin
from .models import User, Role, Staff, Customer, Product, Warehouse, Region, Branch, Order, Archive

# Register your models here.
admin.site.register(User)
admin.site.register(Role)
admin.site.register(Staff)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Warehouse)
admin.site.register(Region)
admin.site.register(Branch)
admin.site.register(Order)
admin.site.register(Archive)
