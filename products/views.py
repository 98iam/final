from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Count, F, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from .forms import ProductForm, CategoryForm

@login_required
def dashboard(request):
    # Filter products by the current user
    total_products = Product.objects.filter(user=request.user).count()
    total_categories = Category.objects.filter(user=request.user).count()
    low_stock_products = Product.objects.filter(user=request.user, quantity__lte=F('minimum_stock')).count()
    total_value = Product.objects.filter(user=request.user).aggregate(
        total=Sum(F('quantity') * F('cost')))['total'] or 0

    recent_products = Product.objects.filter(user=request.user).order_by('-created_at')[:5]
    categories_with_counts = Category.objects.filter(user=request.user).annotate(
        product_count=Count('products')).order_by('-product_count')[:5]

    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'low_stock_products': low_stock_products,
        'total_value': total_value,
        'recent_products': recent_products,
        'categories_with_counts': categories_with_counts,
    }
    return render(request, 'products/dashboard.html', context)

@login_required
def product_list(request):
    # Filter products by the current user
    products = Product.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(sku__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Category filter
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    # Status filter
    status = request.GET.get('status')
    if status:
        products = products.filter(status=status)

    # Low stock filter
    if request.GET.get('low_stock'):
        products = products.filter(quantity__lte=F('minimum_stock'))

    products = products.select_related('category').order_by('name')

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'products/product_list.html', context)

@login_required
def product_detail(request, pk):
    # Ensure the product belongs to the current user
    product = get_object_or_404(Product, pk=pk, user=request.user)
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            try:
                product = form.save(commit=False)
                product.user = request.user
                product.save()
                messages.success(request, f'Product "{product.name}" created successfully.')
                return redirect('product_list')
            except Exception as e:
                messages.error(request, f'Error saving product: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
            # Print form errors for debugging
            print("Form errors:", form.errors)
    else:
        form = ProductForm()

    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Create Product'
    })

@login_required
def product_edit(request, pk):
    # Ensure the product belongs to the current user
    product = get_object_or_404(Product, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Edit Product'})

@login_required
def category_list(request):
    # Filter categories by the current user
    categories = Category.objects.filter(user=request.user).annotate(
        product_count=Count('products')).order_by('name')
    return render(request, 'products/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            try:
                category = form.save(commit=False)
                category.user = request.user
                category.save()
                messages.success(request, f'Category "{category.name}" created successfully.')
                return redirect('category_list')
            except Exception as e:
                messages.error(request, f'Error saving category: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm()

    return render(request, 'products/category_form.html', {
        'form': form,
        'title': 'Create Category'
    })
# Create your views here.
