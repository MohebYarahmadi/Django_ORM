from django.db import models

# -------------------------------------
# Category Model
# -------------------------------------
class Category(models.Model):
	pass

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
	pass


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
