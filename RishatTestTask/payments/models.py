from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Discount(models.Model):
    name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Tax(models.Model):
    name = models.CharField(max_length=50)
    rate = models.DecimalField(max_digits=5, decimal_places=2)

class Order(models.Model):
    items = models.ManyToManyField(Item)
    discount = models.ManyToManyField(Discount, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def calculate_total_price(self):
        item_total = sum(item.price for item in self.items.all())
        discount = self.discount.first()
        discount_total = item_total * (discount.amount / 100)
        self.total_price = item_total - discount_total
        self.save()