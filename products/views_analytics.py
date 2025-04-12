from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count, F, Q, Avg
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.core.serializers.json import DjangoJSONEncoder
import json
from datetime import datetime, timedelta
import random  # For demo data
from decimal import Decimal

from .models import Product, Category, Sale, SaleItem, InventorySnapshot, SavedReport, UserPreference

@login_required
def sales_trends(request):
    # Get date range from request or use default (last 30 days)
    days = int(request.GET.get('days', 30))
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)

    # Get sales data for the period
    sales = Sale.objects.filter(
        user=request.user,
        sale_date__date__gte=start_date,
        sale_date__date__lte=end_date
    ).order_by('sale_date')

    # For demo purposes, if no sales data exists, create some random data
    if not sales.exists():
        sales_data = generate_demo_sales_data(request.user, days)
    else:
        # Group sales by date
        sales_by_date = {}
        for sale in sales:
            date_str = sale.sale_date.date().strftime('%Y-%m-%d')
            if date_str in sales_by_date:
                sales_by_date[date_str] += sale.total_amount
            else:
                sales_by_date[date_str] = sale.total_amount

        # Create a list of dates and corresponding sales amounts
        dates = []
        amounts = []
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            dates.append(date_str)
            amounts.append(float(sales_by_date.get(date_str, 0)))
            current_date += timedelta(days=1)

        sales_data = {
            'dates': dates,
            'amounts': amounts
        }

    context = {
        'sales_data': json.dumps(sales_data, cls=DecimalEncoder),
        'days': days,
        'total_sales': sum(sales_data['amounts']),
        'avg_daily_sales': sum(sales_data['amounts']) / len(sales_data['amounts']) if sales_data['amounts'] else 0
    }

    return render(request, 'products/analytics/sales_trends.html', context)

@login_required
def inventory_value(request):
    # Get date range from request or use default (last 30 days)
    days = int(request.GET.get('days', 30))
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)

    # Get inventory snapshots for the period
    snapshots = InventorySnapshot.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lte=end_date
    ).order_by('date')

    # For demo purposes, if no snapshot data exists, create some random data
    if not snapshots.exists():
        inventory_data = generate_demo_inventory_data(request.user, days)
    else:
        # Create a list of dates and corresponding inventory values
        dates = []
        values = []
        for snapshot in snapshots:
            dates.append(snapshot.date.strftime('%Y-%m-%d'))
            values.append(float(snapshot.total_value))

        inventory_data = {
            'dates': dates,
            'values': values
        }

    # Calculate current inventory value
    current_value = Product.objects.filter(user=request.user).aggregate(
        total=Sum(F('quantity') * F('cost')))['total'] or 0

    context = {
        'inventory_data': json.dumps(inventory_data, cls=DecimalEncoder),
        'days': days,
        'current_value': current_value,
        'change_percentage': calculate_change_percentage(inventory_data['values'])
    }

    return render(request, 'products/analytics/inventory_value.html', context)

@login_required
def product_performance(request):
    # Get top and bottom performing products
    products = Product.objects.filter(user=request.user)

    # For demo purposes, if no sales data exists, create some random data
    if not SaleItem.objects.filter(product__user=request.user).exists():
        performance_data = generate_demo_performance_data(products)
    else:
        # Get sales data for each product
        product_sales = {}
        for product in products:
            sales_count = SaleItem.objects.filter(product=product).aggregate(
                total_quantity=Sum('quantity'),
                total_revenue=Sum(F('quantity') * F('price'))
            )
            product_sales[product.id] = {
                'name': product.name,
                'quantity': sales_count['total_quantity'] or 0,
                'revenue': float(sales_count['total_revenue'] or 0),
                'profit_margin': product.profit_margin
            }

        # Sort products by revenue
        sorted_products = sorted(product_sales.values(), key=lambda x: x['revenue'], reverse=True)

        performance_data = {
            'products': [p['name'] for p in sorted_products],
            'quantities': [p['quantity'] for p in sorted_products],
            'revenues': [p['revenue'] for p in sorted_products],
            'margins': [p['profit_margin'] for p in sorted_products]
        }

    # Convert Decimal objects to float for JSON serialization
    context = {
        'performance_data': json.dumps(performance_data, cls=DecimalEncoder),
        'top_products': get_top_products(performance_data, 5),
        'bottom_products': get_bottom_products(performance_data, 5)
    }

    return render(request, 'products/analytics/product_performance.html', context)

@login_required
def custom_reports(request):
    # Get saved reports for the user
    saved_reports = SavedReport.objects.filter(user=request.user).order_by('-updated_at')

    context = {
        'saved_reports': saved_reports,
        'report_types': SavedReport.REPORT_TYPES
    }

    return render(request, 'products/analytics/custom_reports.html', context)

@login_required
@require_POST
def save_report(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        report_type = data.get('report_type')
        configuration = data.get('configuration', {})

        if not name or not report_type:
            return JsonResponse({'success': False, 'error': 'Missing required fields'})

        # Create or update report
        report, created = SavedReport.objects.update_or_create(
            user=request.user,
            name=name,
            defaults={
                'report_type': report_type,
                'configuration': configuration
            }
        )

        return JsonResponse({'success': True, 'report_id': report.id})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def save_theme_preference(request):
    try:
        data = json.loads(request.body)
        theme = data.get('theme')

        if theme not in ['light', 'dark']:
            return JsonResponse({'success': False, 'error': 'Invalid theme'})

        # Update or create user preference
        preference, created = UserPreference.objects.update_or_create(
            user=request.user,
            defaults={'theme': theme}
        )

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

# Helper functions for demo data
def generate_demo_sales_data(user, days):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)

    dates = []
    amounts = []

    current_date = start_date
    base_amount = random.uniform(100, 500)

    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        # Generate a somewhat realistic sales pattern with weekends having higher sales
        weekday = current_date.weekday()
        weekend_factor = 1.5 if weekday >= 5 else 1.0
        daily_variation = random.uniform(0.7, 1.3)
        amount = base_amount * weekend_factor * daily_variation

        dates.append(date_str)
        amounts.append(round(amount, 2))

        current_date += timedelta(days=1)

    return {
        'dates': dates,
        'amounts': amounts
    }

def generate_demo_inventory_data(user, days):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)

    dates = []
    values = []

    current_date = start_date
    base_value = random.uniform(5000, 20000)
    trend = random.choice([-1, 1])  # Decreasing or increasing trend

    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        # Generate a somewhat realistic inventory pattern with gradual changes
        daily_variation = random.uniform(0.98, 1.02)
        trend_factor = 1 + (0.005 * trend)
        base_value = base_value * daily_variation * trend_factor

        dates.append(date_str)
        values.append(round(base_value, 2))

        current_date += timedelta(days=1)

    return {
        'dates': dates,
        'values': values
    }

# Custom JSON encoder to handle Decimal objects
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def generate_demo_performance_data(products):
    product_names = []
    quantities = []
    revenues = []
    margins = []

    for product in products:
        product_names.append(product.name)
        quantity = random.randint(5, 100)
        price = float(product.price)
        revenue = quantity * price

        quantities.append(quantity)
        revenues.append(round(revenue, 2))
        margins.append(round(float(product.profit_margin), 2))

    return {
        'products': product_names,
        'quantities': quantities,
        'revenues': revenues,
        'margins': margins
    }

def calculate_change_percentage(values):
    if not values or len(values) < 2:
        return 0

    first_value = values[0]
    last_value = values[-1]

    if first_value == 0:
        return 100  # Avoid division by zero

    return round(((last_value - first_value) / first_value) * 100, 2)

def get_top_products(data, count):
    if not data or 'products' not in data or 'revenues' not in data:
        return []

    # Combine product names and revenues
    products = list(zip(data['products'], data['revenues']))

    # Sort by revenue (descending)
    sorted_products = sorted(products, key=lambda x: x[1], reverse=True)

    # Return top N products
    return sorted_products[:count]

def get_bottom_products(data, count):
    if not data or 'products' not in data or 'revenues' not in data:
        return []

    # Combine product names and revenues
    products = list(zip(data['products'], data['revenues']))

    # Sort by revenue (ascending)
    sorted_products = sorted(products, key=lambda x: x[1])

    # Return bottom N products
    return sorted_products[:count]
