from django.contrib import admin

from .models import Product, ProductPromotion, Promotion, OrderLine, Order, VendorCommission

admin.site.register([Product, ProductPromotion, Promotion, OrderLine, Order, VendorCommission])

