from typing import Optional, List
from ninja import Router, Schema
from django.utils.text import slugify
from datetime import datetime

from inventory.models import (
	Category, Product, StockManagement,
    Order, OrderProduct, User
)

router = Router()


#region GENERAL SCHEMAS
# ==========================================
# Schema: 404 Error Schema
# ==========================================
class ErrorResponse(Schema):
	detail: str

#endregion


#region CATEGORY
# ==========================================
# Schema: Category Out
# ==========================================
class CategoryOut(Schema):
	id: int
	name: str
	slug: str
	is_active: bool
	level: int
	parent_id: int | None = None


@router.get(
	'/category/all',
	tags=['module5'],
	summary='Retrieve all categories',
	response=List[CategoryOut]
)
def get_all_categories(request):
	return Category.objects.all()


# ==========================================
# Schema: Return name & slug only
# ==========================================
class CategoryNameSlugOut(Schema):
	name: str
	slug: str


@router.get(
	'/category/all-name-slug',
	tags=['module5'],
	summary='Retrieve all categories with name and slug only',
	response=List[CategoryNameSlugOut]
)
def get_category_names(request):
	# return list(Category.objects.values('name', 'slug'))
	
	queryset = Category.objects.values('name', 'slug')
	# Optional: Modify or preprocess data
	results = [
		{'name': item['name'].upper(), 'slug': item['slug']} for item in queryset
	]

	return results


# ==========================================
# Schema: Returns name & slug using only()
# ==========================================
class CategoryNameSlugOnlyOut(Schema):
	name: str
	slug: str


@router.get(
	'/category/names-optimized',
	tags=['module5'],
	summary='Retrieve category names and slug using only()',
	response=List[CategoryNameSlugOnlyOut]
)
def get_category_names_optimized(request):
	queryset = Category.objects.only('name', 'slug')

	# Prepare data manually from model instances
	results = [
		{'name': category.name, 'slug': category.slug} for category in queryset
	]
	return results


# ==========================================
# Schema: Filter inactive name & slug using only() and filter()
# ==========================================
class CategoryActiveNameSlugOut(Schema):
	name: str
	slug: str


@router.get(
	'/category/inactive-names',
	tags=['module5'],
	summary='Retrieve inactive category names and slug using only() and filter()',
	response={200: List[CategoryActiveNameSlugOut], 404: ErrorResponse},
)
def get_inactive_category_names(request):
	# queryset = Category.objects.only('name', 'slug').filter(is_active=False)
	queryset = Category.objects.only('name', 'slug').filter(name='Nothing There')	# Return 404

	if not queryset.exists():
		return 404, {'detail': 'No inactive categories found with that name.'}

	# Prepare data manually from model instances
	results = [
		{'name': category.name, 'slug': category.slug} for category in queryset
	]
	return results


# ==========================================
# Schema: Exclude archived categories, retun name & slug
# ==========================================
class CategoryNameSlugArchivedOut(Schema):
	name: str
	slug: str


@router.get(
	'/category/active-excluding-archived',
	tags=['module5'],
	summary="Retrieve active categories excluding 'Archived'",
	response={200: List[CategoryNameSlugArchivedOut], 404: ErrorResponse},
)
def get_active_non_archived_categories(request):
	queryset = (
		Category.objects.only('name', 'slug')
		.filter(is_active=True)
		.exclude(name='Archived')
		.order_by('name')
	)

	if not queryset.exists():
		return 404, {'detail': 'No active categories found excluding "Archived".'}

	results = [
		{'name': category.name, 'slug': category.slug} for category in queryset
	]

	return results


# ==========================================
# Schema: Get first/last active cat by name (ASC)
# ==========================================
class CategoryFirstOut(Schema):
	name: str
	slug: str


@router.get(
	'/category/first-active',
	tags=['module5'],
	summary='Retrieve the first/last active category by name ASC',
	response={200: CategoryFirstOut, 404: ErrorResponse}
)
def get_first_active_cat_by_name(request):
	category = (
		Category.objects.only('name', 'slug')
		.filter(is_active=True)
		.order_by('name')
		.first()
		# .last()
	)

	if category is None:
		return 404, {'detail': 'No active categories found.'}

	return {'name': category.name, 'slug': category.slug}

#endregion

#region PRODUCTS
# ==========================================
# Schema: Product Get All Sorted Out
# ==========================================
class ProductAllSortedOut(Schema):
	id: int
	name: str
	slug: str
	description: str
	is_digital: bool
	is_active: bool
	price: float

@router.get(
	'/product/all',
	tags=['Challenge'],
	summary='Get all products sorted by name DSC',
	response=List[ProductAllSortedOut],
)
def get_all_products_sorted(request):
	queryset = Product.objects.all().filter(is_active=True).order_by('-name')

	if not queryset.exists():
		return {'error': 'There is no product'}

	return queryset


# ==========================================
# Schema: Product Onlu Name and Price Ordered
# ==========================================
class ProductOnlyNamePriceOut(Schema):
	name: str
	price: float


@router.get(
	'/product/only-name-price',
	tags=['Challenge'],
	summary='Get all products with only name and price ordered by price DSC',
	response=List[ProductOnlyNamePriceOut],
)
def get_product_only_name_price(request):
	queryset = Product.objects.only('name', 'price').order_by('-price')

	if not queryset.exists():
		return {'error': 'There is no product'}

	return queryset


# ==========================================
# Schema: Product First Created
# ==========================================
class ProductFirstOut(Schema):
	id: int
	name: str
	slug: str
	description: str
	price: float
	# created_at: datetime	# Don't need to be included
	# ...to use as order_by


@router.get(
	'/product/get-first',
	tags=['Challenge'],
	summary='Get the frist products created by data',
	response={200: ProductFirstOut, 404: ErrorResponse},
)
def get_first_product(request):
	queryset = Product.objects.order_by('created_at').first()	# First
	# queryset = Product.objects.order_by('-created_at').first() # Most recently added

	if queryset is None:
		return 404, {'detail', 'No match found'}

	return queryset
	

# ==========================================
# Schema: Product Most Recently
# ==========================================


#endregion