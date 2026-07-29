from django.db import models
from django.db.models import UniqueConstraint

# -------------------------------------
# Category Model
# -------------------------------------


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=55, unique=True)
    is_active = models.BooleanField(default=False)
    level = models.SmallIntegerField(default=0)

    # Relations
    parent = models.ForeignKey(
        'self', on_delete=models.RESTRICT, null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'categories'
        db_table = 'category'
        ordering = ["-name"]

    def __str__(self):
        return f'{self.id}-{self.name}'

# -------------------------------------
# Custom Enumeration Classes
# -------------------------------------
class DiscountLevel(models.IntegerChoices):
    TEN = 10, "10%"
    TWENTY = 20, "20%"
    FIFTY = 50, "50%"


class Status(models.TextChoices):
    PENDING = "PEN", "Pending"
    APPROVED = "APP", "Approved"
    REJECTED = "REJ", "Rejected"


# -------------------------------------
# Promotion Event Model
# -------------------------------------
class PromotionEvent(models.Model):
    name = models.CharField(max_length=50, unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    price_reduction = models.IntegerField(
        choices=DiscountLevel.choices,)  # Use our Custom Enumeration Class

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.name

# -------------------------------------
# Product Model
# -------------------------------------
class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=55, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_digital = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    # Relations
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name="products")
    promotion_events = models.ManyToManyField(
        PromotionEvent,
        through="ProductPromotionEvent",  # use our custom link model
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

# -------------------------------------
# Product Promotion Event Model (-M:M-Custom Link Model-)
# -------------------------------------
class ProductPromotionEvent(models.Model):  # our custom link model
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    promotion_event = models.ForeignKey(
        PromotionEvent, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["product", "promotion_event"],
                name="unique_product_per_promotion_event",
            )
        ]

    def __str__(self):
        return f"{self.product.name} – {self.promotion_event.name}"

# -------------------------------------
# Stock Management Model
# -------------------------------------
class StockManagement(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        unique=True,
        related_name="stock",
    )
    quantity = models.IntegerField(default=0)
    last_checked_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Stock: {self.product.name} – {self.quantity} units"

# -------------------------------------
# User Model
# -------------------------------------


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=60)

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return self.username


# -------------------------------------
# Order Model
# -------------------------------------
class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relations
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


# -------------------------------------
# Order Product Model
# -------------------------------------
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        unique_together = ("product", "order")

    def __str__(self):
        return f"{self.product.name} x{self.quantity} in Order {self.order.id}"