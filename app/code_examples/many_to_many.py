# reverse_joins.py

# Usage:
# docker compose up --build -d
# docker exec -it django_app sh -c "clear && python manage.py shell_plus"


import os

from django.db import connection, reset_queries
from django.db.models import Prefetch
from inventory.models import Order, Product


def cls():
    os.system("clear")


def pretty_all():
    from sqlparse import format

    for q in connection.queries:
        print("→")
        print(format(q["sql"], reindent=True, keyword_case="upper"))


def show_queries():
    print("Queries run:", len(connection.queries))


# 🔹 ex19 – Get all products in a given order
def ex19():
    """List products in a specific order"""
    reset_queries()
    order = Order.objects.get(id=1)
    print(f"Order ID: {order.id}")

    for p in order.products.all():
        print(p.name)
    show_queries()
    pretty_all()


# 🔹 ex20 List products in a specific order, including user who placed it
def ex20():
    """List products in a specific order, including user who placed it"""
    reset_queries()

    order = Order.objects.select_related("user").get(id=1)
    print(f"Order ID: {order.id} — Placed by: {order.user.username}")

    for p in order.products.all():
        print(p.name)

    show_queries()
    pretty_all()


# 🔹 ex21 List products in a specific order, including user and product category
def ex21():
    """List products in a specific order, including user and product category"""
    reset_queries()

    order = (
        Order.objects.select_related("user")
        .prefetch_related(
            Prefetch("products", queryset=Product.objects.select_related("category"))
        )
        .get(id=1)
    )

    print(f"Order ID: {order.id} — Placed by: {order.user.username}")

    for product in order.products.all():
        print(f"{product.name} — Category: {product.category.name}")

    show_queries()
    pretty_all()


# 🔹 ex22 – Get all orders containing a specific product
def ex22():
    """Find all orders that contain a specific product"""
    reset_queries()
    product = Product.objects.get(slug="iphone-13")
    for order in product.order_set.all():
        print(f"Order {order.id}")
    show_queries()
    pretty_all()


# 🔹 ex23 – Get all OrderProduct entries for a specific order
def ex23():
    """Show products with quantities in an order (through model)"""
    reset_queries()
    order = Order.objects.get(id=1)
    for op in order.orderproduct_set.select_related("product"):
        print(op.product.name, "x", op.quantity)
    show_queries()
    pretty_all()


# 🔹 ex24 – Get order with full product and stock info
def ex24():
    """Get products and stock details for an order"""
    reset_queries()
    order = Order.objects.first()
    for op in order.orderproduct_set.select_related("product__stock"):
        product = op.product
        print(f"{product.name} x{op.quantity} – Stock: {product.stock.quantity}")
    show_queries()
    pretty_all()


# 🔹 ex25 – Get orders that include products with low stock
def ex25():
    """Find orders that contain products with stock < 40"""
    reset_queries()
    qs = Order.objects.filter(products__stock__quantity__lt=40).distinct()
    for order in qs:
        print(f"Order {order.id}")
    show_queries()
    pretty_all()


# 🔹 ex26 – Get product category info in an order
def ex26():
    """Display category of each product in an order"""
    reset_queries()
    order = Order.objects.first()
    for op in order.orderproduct_set.select_related("product__category"):
        p = op.product
        print(f"{p.name} ({p.category.name}) x{op.quantity}")
    show_queries()
    pretty_all()
