from django.contrib import admin
from product.models import *
admin.site.register(Products)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Address)