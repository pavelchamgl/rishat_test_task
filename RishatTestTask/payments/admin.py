from django.contrib import admin

from .models import Item, Order, Tax, Discount

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Tax)
admin.site.register(Discount)
