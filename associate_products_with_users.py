import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invent.settings')
django.setup()

from django.contrib.auth.models import User
from products.models import Product, Category

def associate_products_with_users():
    # Get the first user or create one if none exists
    try:
        first_user = User.objects.first()
        if not first_user:
            # Create a default user if no users exist
            first_user = User.objects.create_user(
                username='admin',
                email='admin@example.com',
                password='adminpassword'
            )
        
        # Associate all existing products with the first user
        products_updated = Product.objects.filter(user__isnull=True).update(user=first_user)
        
        # Associate all existing categories with the first user
        categories_updated = Category.objects.filter(user__isnull=True).update(user=first_user)
        
        print(f"Updated {products_updated} products and {categories_updated} categories.")
        
    except Exception as e:
        print(f"Error associating products with users: {e}")

if __name__ == "__main__":
    associate_products_with_users()
