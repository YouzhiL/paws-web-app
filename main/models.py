from random import random
import string
from tkinter import CASCADE
from turtle import ondrag
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from django_extensions.db.fields import AutoSlugField

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class CustomUser(AbstractUser):
    mailing_address = models.CharField(max_length=200, blank=True)
    balance = models.FloatField(default=200.0)
    is_seller = models.BooleanField(default=False)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ProductFB(models.Model):
    # product = models.ForeignKey(General_Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    israted = models.BooleanField(default=False)
    rating = models.IntegerField(blank = True, null=True)
    review = models.CharField(blank=True, null=True, max_length=1024)

class General_Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_img = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, default=False, null=True, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    slug = AutoSlugField(populate_from=['product_name'])
    feedback = models.ManyToManyField(ProductFB)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={'slug': self.slug})
    
    def get_product_feedback_url(self):
        return reverse("product_feedback", kwargs={
            'slug': self.slug
        })
    def get_rating(self):
        total = 0
        count = 0
        for fb in self.feedback.all():
            total += fb.rating
            count += 1
        if count == 0:
            return None
        return total/count




class Product(models.Model):
    general_product = models.ForeignKey(General_Product, blank = True, null = True, on_delete=models.CASCADE)
    price = models.FloatField(default=0.0)
    discount_price = models.FloatField(blank=True, null=True)
    quantity = models.IntegerField(default=0)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from=['general_product', 'seller'])


    def __str__(self):
        return self.general_product.product_name

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'slug': self.slug
        })
    def edit_inventory_url(self):
        return reverse("edit-inventory", kwargs={
            'slug': self.slug
        })
    

    






class OrderItem(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    fulfilled = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    # date = models.DateTimeField('date purchased')
    # def __str__(self):
    #     return "Order# " + str(self.order_id)
    def __str__(self):
        return f"{self.quantity} of {self.product.general_product.product_name}"

    def get_total_item_price(self):
        return self.quantity * self.product.price

    def get_total_discount_item_price(self):
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()
    


# class Sub_Order(models.Model):
#     items = models.ManyToManyField
class Order(models.Model):
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    # seller_order = models.ManyToManyField(SellerOrder)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    # payment = models.ForeignKey(
    #     'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    fulfilled = models.BooleanField(default=False)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from=['user', 'ordered_date'])

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total
    def get_numOfItem(self):
        total = 0
        for order_item in self.items.all():
            total += 1
        return total

    def get_absolute_url(self):
        return reverse("detailed-order-page", kwargs={'slug': self.slug})
    def get_seller_url(self):
        return reverse("seller-detail-order", kwargs={'slug': self.slug})

class Address(models.Model):
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(CustomUser,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code

class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

class Cart(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)


    

