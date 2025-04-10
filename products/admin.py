from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'product_count', 'created_at')
    search_fields = ('name', 'description')
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Number of Products'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'price', 'quantity_status', 'status')
    list_filter = ('category', 'status', 'created_at')
    search_fields = ('name', 'sku', 'description', 'supplier')
    readonly_fields = ('created_at', 'updated_at')  # Remove profit_margin from readonly_fields
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'status')
        }),
        ('Product Details', {
            'fields': ('sku', 'barcode', 'supplier', 'location')
        }),
        ('Stock Information', {
            'fields': ('quantity', 'minimum_stock', 'maximum_stock')
        }),
        ('Financial Information', {
            'fields': ('price', 'cost')  # Remove profit_margin from here
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def quantity_status(self, obj):
        status = obj.stock_status
        if status == "Low Stock":
            color = "red"
        elif status == "Overstocked":
            color = "orange"
        else:
            color = "green"
        return format_html('<span style="color: {};">{} ({})</span>',
                         color,
                         obj.quantity,
                         status)
    quantity_status.short_description = 'Quantity (Status)'


