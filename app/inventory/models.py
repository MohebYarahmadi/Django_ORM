from django.db import models

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
	description = models.TextField()
	price = models.DecimalField(max_digits=10, decimal_places=2)


# -------------------------------------
# Product Promotion Event Model
# -------------------------------------
class ProductPromotionEvent(models.Model):
	pass


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
	pass
