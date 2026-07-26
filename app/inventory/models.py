from django.db import models
from django.db.models import UniqueConstraint

# -------------------------------------
# Category Model
# -------------------------------------
class Category(models.Model):
	name  = models.CharField(max_length=50)
	is_active = models.BooleanField(default=False)
	level = models.SmallIntegerField()

	class Meta:
		db_table = 'category'


# -------------------------------------
# Promotion Event Model
# -------------------------------------
class PromotionEvent(models.Model):
	pass


# -------------------------------------
# Product Model
# -------------------------------------
class Product(models.Model):
	name = models.CharField(max_length=50, unique=True)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	slug = models.SlugField(max_length=55, unique=True)
	is_digital = models.BooleanField(default=False)
	is_active = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	updated_at = models.DateTimeField(auto_now=True)

	# Relations
	category = models.ForeignKey(Category, on_delete=models.RESTRICT)
	promotion_events = models.ManyToManyField(
		PromotionEvent,
		through="ProductPromotionEvent",	# use our custom link model
	)


# -------------------------------------
# Product Promotion Event Model (-M:M-Custom Link Model-)
# -------------------------------------
class ProductPromotionEvent(models.Model):	# our custom link model
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	promotion_event = models.ForeignKey(PromotionEvent, on_delete=models.CASCADE)

	class Meta:
		constraints = [
			UniqueConstraint(
				fields=["product", "promotion_event"],
				name="unique_product_per_category",
			)
		]


# -------------------------------------
# Stock Management Model
# -------------------------------------
class StockManagement(models.Model):
	pass


# -------------------------------------
# User Model
# -------------------------------------
class User(models.Model):
	pass


# -------------------------------------
# Order Model
# -------------------------------------
class Order(models.Model):
	pass


# -------------------------------------
# Order Product Model
# -------------------------------------
class OrderProduct(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField()

	class Meta:
		constraints = [
			UniqueConstraint(
				fields=["product", "order"], name="unique_product_per_category"
			)
		]
