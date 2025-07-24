import os
import django
import random

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_graphql_crm.settings")
django.setup()

from crm.models import Customer, Product, Order

def seed():
    print("🧹 Clearing existing data...")
    Order.objects.all().delete()
    Product.objects.all().delete()
    Customer.objects.all().delete()

    print("👥 Creating customers...")
    customers = []
    for i in range(10):
        customer = Customer.objects.create(
            name=f"Customer {i}",
            email=f"customer{i}@example.com",
            phone=f"+1234567890{i}"
        )
        customers.append(customer)

    print("📦 Creating products...")
    products = []
    for i in range(5):
        product = Product.objects.create(
            name=f"Product {i}",
            description=f"Description for product {i}",
            price=random.randint(100, 1000)
        )
        products.append(product)

    print("🧾 Creating orders...")
    for _ in range(20):
        Order.objects.create(
            customer=random.choice(customers),
            product=random.choice(products),
            quantity=random.randint(1, 5),
            status=random.choice(["pending", "shipped", "delivered"])
        )

    print("✅ Seeding complete.")

if __name__ == "__main__":
    seed()
