from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .models import UserPreference

@login_required
def dashboard_settings(request):
    """View for dashboard customization settings"""
    # Get or create user preferences
    preference, created = UserPreference.objects.get_or_create(user=request.user)
    
    # Get widget configurations
    widgets = preference.dashboard_widgets or preference.DEFAULT_DASHBOARD_WIDGETS
    
    # Define widget display names and descriptions
    widget_info = {
        'total_products': {
            'name': 'Total Products',
            'description': 'Shows the total number of products in your inventory.'
        },
        'total_categories': {
            'name': 'Total Categories',
            'description': 'Shows the total number of product categories.'
        },
        'low_stock_products': {
            'name': 'Low Stock Products',
            'description': 'Shows the number of products with stock below minimum level.'
        },
        'total_value': {
            'name': 'Total Inventory Value',
            'description': 'Shows the total value of your current inventory.'
        },
        'recent_products': {
            'name': 'Recent Products',
            'description': 'Shows a list of recently added products.'
        },
        'categories_with_counts': {
            'name': 'Categories Overview',
            'description': 'Shows categories with their product counts.'
        },
    }
    
    # Combine widget configurations with their info
    widget_data = []
    for widget_id, config in widgets.items():
        info = widget_info.get(widget_id, {'name': widget_id, 'description': ''})
        widget_data.append({
            'id': widget_id,
            'name': info['name'],
            'description': info['description'],
            'enabled': config.get('enabled', True),
            'order': config.get('order', 999)
        })
    
    # Sort widgets by their order
    widget_data.sort(key=lambda x: x['order'])
    
    context = {
        'widget_data': widget_data,
    }
    
    return render(request, 'products/dashboard_settings.html', context)

@login_required
@require_POST
def save_dashboard_settings(request):
    """Save dashboard widget settings"""
    try:
        data = json.loads(request.body)
        widgets_config = data.get('widgets', {})
        
        # Get or create user preferences
        preference, created = UserPreference.objects.get_or_create(user=request.user)
        
        # Update widget configurations
        current_widgets = preference.dashboard_widgets or preference.DEFAULT_DASHBOARD_WIDGETS
        
        for widget_id, config in widgets_config.items():
            if widget_id in current_widgets:
                current_widgets[widget_id]['enabled'] = config.get('enabled', True)
                current_widgets[widget_id]['order'] = config.get('order', 999)
        
        # Save updated configurations
        preference.dashboard_widgets = current_widgets
        preference.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def reset_dashboard_settings(request):
    """Reset dashboard widget settings to defaults"""
    try:
        # Get user preferences
        preference, created = UserPreference.objects.get_or_create(user=request.user)
        
        # Reset to defaults
        preference.dashboard_widgets = preference.DEFAULT_DASHBOARD_WIDGETS
        preference.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
