from typing import Optional, List
from ninja import Router, Schema
from django.utils.text import slugify

from inventory.models import (
	Category, Product, StockManagement,
    Order, OrderProduct, User
)

router = Router()

#region CATEGORY
# ==========================================
# Schema: 404 Error Schema
# ==========================================
class ErrorResponse(Schema):
	detail: str


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

#endregion

