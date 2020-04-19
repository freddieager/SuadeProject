from django.db import models


class Order(models.Model):
    created_at = models.DateTimeField()
    vendor_id = models.IntegerField(null=True)
    customer_id = models.IntegerField(null=True)


class OrderLine(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    product_description = models.TextField()
    product_price = models.FloatField()
    product_vat_rate = models.FloatField()
    discount_rate = models.FloatField()
    quantity = models.IntegerField()
    full_price_amount = models.FloatField()
    discounted_amount = models.FloatField()
    vat_amount = models.FloatField()
    total_amount = models.FloatField()


class Product(models.Model):
    description = models.TextField(null=True)


class Promotion(models.Model):
    description = models.TextField(null=True)


class ProductPromotion(models.Model):
    date = models.DateTimeField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    promotion = models.ForeignKey('Promotion', on_delete=models.CASCADE)


class VendorCommission(models.Model):
    date = models.DateTimeField()
    vendor_id = models.IntegerField(null=True)
    rate = models.FloatField()
