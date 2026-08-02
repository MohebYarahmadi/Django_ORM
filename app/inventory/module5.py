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


#endregion

