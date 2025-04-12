from django.urls import path
from . import views
from . import views_analytics

urlpatterns = [
    # Main views
    path('', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),

    # Analytics views
    path('analytics/sales-trends/', views_analytics.sales_trends, name='sales_trends'),
    path('analytics/inventory-value/', views_analytics.inventory_value, name='inventory_value'),
    path('analytics/product-performance/', views_analytics.product_performance, name='product_performance'),
    path('analytics/custom-reports/', views_analytics.custom_reports, name='custom_reports'),
    path('save-report/', views_analytics.save_report, name='save_report'),
    path('save-theme-preference/', views_analytics.save_theme_preference, name='save_theme_preference'),
]