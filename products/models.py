from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

class Product(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('discontinued', 'Discontinued'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    sku = models.CharField(max_length=50, unique=True, verbose_name="SKU")
    barcode = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="Purchase cost per unit")
    quantity = models.IntegerField(default=0)
    minimum_stock = models.IntegerField(default=0, help_text="Minimum stock level before reorder")
    maximum_stock = models.IntegerField(default=0, help_text="Maximum stock level")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    location = models.CharField(max_length=100, blank=True, null=True, help_text="Storage location")
    supplier = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.minimum_stock > self.maximum_stock:
            raise ValidationError("Minimum stock cannot be greater than maximum stock")
        if self.quantity < 0:
            raise ValidationError("Quantity cannot be negative")

    @property
    def stock_status(self):
        if self.quantity <= self.minimum_stock:
            return "Low Stock"
        elif self.quantity >= self.maximum_stock:
            return "Overstocked"
        return "Normal"

    @property
    def profit_margin(self):
        try:
            if self.cost and self.cost > 0:
                return ((self.price - self.cost) / self.cost) * 100
            return 0
        except (TypeError, ZeroDivisionError):
            return 0

