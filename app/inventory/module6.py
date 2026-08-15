from pyclbr import Class
from typing import Optional, List
from django.db.models import Q
from ninja import Router, Schema, Query
from django.utils.text import slugify
from datetime import datetime, timedelta
from django.utils.timezone import now

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
# Schema: Filter categories by active status, level range, parent existence
# ==========================================
class ParentCategoryOut(Schema):
	id: int
	name: str
	slug: str


class CategoryOut(Schema):
	id: int
	name: str
	slug: str
	level: int
	is_active: bool
	# parent: Optional[ParentCategoryOut]	# Will populated by the full instance
	# parent_id: Optional[int]	# Will get integer id automatically
	parent: Optional[int] # Will populated using @staticmethod


	@staticmethod
	def resolve_parent(obj):
		return obj.parent.id if obj.parent else None


@router.get(
	'/categories/',
	tags=['module6'],
	summary='Filter categories by is_active, level range and parent presence',
	response=List[CategoryOut]
)
def get_filtered_categories(
	request,
	active: bool = None,
	min_level: int = None,
	max_level: int = None,
	has_parent: bool = None,
):
	qs = Category.objects.all()

	if active is not None:
		qs = qs.filter(is_active=active)

	if min_level is not None:
		qs = qs.filter(level__gte=min_level)

	if max_level is not None:
		qs = qs.filter(level__lte=max_level)

	if has_parent is not None:
		if has_parent:
			qs = qs.filter(parent__isnull=False)
		else:
			qs = qs.filter(parent__isnull=True)

	return qs

# ==========================================
# Schema: Filter categories by active status, level range, parent existence Q Object
# ==========================================
class CategoryQOut(Schema):
	id: int
	name: str
	slug: str
	level: int
	is_active: bool
	parent_id: Optional[int]

@router.get(
	'/categories/q/combined',
	tags=['module6'],
	summary='Filter categories using Q object combinations (AND / OR logic)',
	response=List[CategoryQOut]
)
def get_filtered_categories_with_q(
	request,
	active: bool = None,
	min_level: int = None,
	max_level: int = None,
	has_parent: bool = None,
	level_match: bool = False,	# New optional flag for OR condition
):
	filters = Q()	# create an empty Q object

	# Base condition: active status
	if active is not None:
		filters &= Q(is_active=active)

	# Build separate condition group: OR between level filters
	level_filter = Q()

	if min_level is not None:
		level_filter |= Q(level__gte=min_level)

	if max_level is not None:
		level_filter |= Q(level__lte=max_level)

	# Apply OR condition only if flag is True and at least one level filter exists
	if level_match and level_filter:
		filters &= level_filter
	else:
		# If not using OR, apply level filters as AND
		if min_level is not None:
			filters &= Q(level__gte=min_level)
		if max_level is not None:
			filters &= Q(level__lte=max_level)


	# Handle parent existence filter
	if has_parent is not None:
		if has_parent:
			filters &= Q(parent__isnull=not has_parent)

	return Category.objects.filter(filters).order_by('level')


# ==========================================
# Schema: Paginate filterd categories by page number
# ==========================================
class PaginateResponse(Schema):
	total: int
	page: int
	page_size: int
	items: list[CategoryOut]

@router.get(
	'/categories/q/paginate',
	tags=['module6'],
	summary='Paginate filtered categories by page number',
	response=PaginateResponse,
)
def paginate_categories_by_page(
	request,
	page: int = Query(1, ge=1),
	page_size: int = Query(10, ge=1, le=100),
	is_active: Optional[bool] = Query(None),
):
	filters = Q()

	if is_active is not None:
		filters &= Q(is_active=is_active)

	qs = Category.objects.filter(filters).order_by('name')

	total = qs.count()
	# Calculate offset from page number
	start = (page - 1) * page_size
	end = start + page_size
	items = qs[start:end]

	return {
		'total': total,
		'page': page,
		'page_size': page_size,
		'items': items
	}


# ==========================================
# Return active categories usin custom manager
# ==========================================
@router.get(
	'/categories/active',
	tags=['module6'],
	summary='Return all active categories using custom manager',
	response=List[CategoryOut]
)
def get_active_categories(request):
	return Category.objects.active().order_by('name')


#endregion CATEGORY


#region PRODUCT
# ==========================================
# Schema: Filter products using Q objec combinations (AND/OR logic)
# ==========================================
class ProductOutCombined(Schema):
	id: int
	name: str
	slug: str
	is_digital: bool
	is_active: bool
	price: float

@router.get(
	'/products/q/combined',
	tags=['module6'],
	summary='Filter products using Q object combinations (AND / OR logic)',
	response=List[ProductOutCombined]
)
def get_filtered_products_with_q(
	request,
	active: bool = None,
	digital_only: bool = None,
	min_price: float = None,
	max_price: float = None,
	price_match: bool = False,
	name_or_slug: Optional[str] = None
):
	filters = Q()

	# Base filter: active flag
	if active is not None:
		filters &= Q(is_active=active)

	# Digital products
	if digital_only is not None:
		filters &= Q(is_digital=digital_only)

	# OR logic for price range
	price_filter = Q()
	if min_price is not None:
		price_filter |= Q(price__gte=min_price)
	if max_price is not None:
		price_filter |= Q(price__lte=max_price)

	if price_match and price_filter:
		filters &= price_filter
	else:
		if min_price is not None:
			filters &= Q(price__gte=min_price)
		if max_price is not None:
			filters &= Q(price__lte=max_price)

	# Search by name or slug using OR
	if name_or_slug:
		filters &= Q(name__icontains=name_or_slug) | Q(slug__icontains=name_or_slug)

	return Product.objects.filter(filters).order_by('name')

# ==========================================
# Schema: Filter products using negation with Q objects
# ==========================================
class ProductOutNegated(Schema):
	id: int
	name: str
	slug: str
	is_digital: bool
	is_active: bool
	price: float

	class Config:
		from_attributes = True

@router.get(
	'/products/q/negated',
	tags=['module6'],
	summary='Filter products using NOT conditions with Q objects.',
	response=List[ProductOutNegated]
)
def get_products_with_negations(
	request,
	active: bool = None,
	exclude_digital: bool = False,
	digital_only: bool = None,
	min_price: float = None,
	max_price: float = None,
	outside_price_range: bool = False,
	exclude_keyword: bool = False,
	# price_match: bool = False,
	name_or_slug: Optional[str] = None
):
	filters = Q()

	# Optionale: only active or inactive
	if active is not None:
		filters &= Q(is_active=True)

	# Exclude digital products if requested
	if digital_only:
		filters &= ~Q(is_digital=digital_only)

	# Price filtering
	if min_price is not None and max_price is not None and outside_price_range:
		# Outside the range = less than min OR greate than max
		filters &= Q(price__lt=min_price) | Q(price__gt=max_price)
	else:
		if min_price is not None:
			filters &= Q(price__gte=min_price)
		if max_price is not None:
			filters &= Q(price__lte=max_price)

	# Keyword filtering on name or slug
	if name_or_slug:
		keyword_filter = Q(name__icontains=name_or_slug) | Q(slug__icontains=name_or_slug)
		filters &= ~keyword_filter if exclude_keyword else keyword_filter

	return Product.objects.filter(filters).order_by('name')



# ==========================================
# Schema: Flexible name pattern filtering
# ==========================================
class ProductOutPatternSearch(Schema):
	id: int
	name: str
	slug: str
	is_digital: bool
	is_active: bool
	price: float

@router.get(
	'/products/q/name-pattern',
	tags=['module6'],
	summary='Filter products by name with selectable pattern matching.',
	response=List[ProductOutPatternSearch]
)
def search_products_by_name_pattern(
	request,
	name: str,
	match_type: str = 'all',	# Options: all, start, end
):
	filters = Q()

	if match_type == 'start':
		filters &= Q(name__istartswith=name)
	elif match_type == 'end':
		filters &= Q(name__iendswith=name)
	else:
		filters &= Q(name__icontains=name)

	return Product.objects.filter(filters).order_by('name')


# ==========================================
# Schema: Filter by ID list and active status
# ==========================================
class ProductOutByIdList(Schema):
	id: int
	name: str
	slug: str
	is_digital: bool
	is_active: bool
	price: float

@router.get(
	'/products/q/by-ids',
	tags=['module6'],
	summary='Filter products by a list of IDs and active status.',
	response=List[ProductOutByIdList]
)
def filter_products_by_ids(
	request,
	ids: List[int] = Query(...),   # Query(required=True)
	inactive: Optional[bool] = None
):
	filters = Q()

	# Filter by provided ID list
	if ids:
		filters &= Q(id__in=ids)
	else:
		return []

	# Optinal: Include only inactive or active products
	if inactive is not None:
		filters &= Q(is_active=not inactive)

	return Product.objects.filter(filters).order_by('name')


# ==========================================
# Schema: Filter by price range
# ==========================================
class ProductOutByPriceRange(Schema):
	id: int
	slug: str
	is_digital: bool
	is_active: bool
	price: float


@router.get(
	'/products/q/by-price-range',
	tags=['module6'],
	summary='Filter products by a specified price range.',
	response=List[ProductOutByPriceRange]
)
def filter_products_by_price_range(
	request,
	min_price: float = Query(..., description="Minimum price for filtering"),
	max_price: float = Query(..., description="Maximum price for filtering"),
	active_only: Optional[bool] = Query(None),
):
	filters = Q(price__range=(min_price, max_price))

	# Optional filter for is_active
	if active_only == True:
		filters &= Q(is_active=True)

	return Product.objects.filter(filters).order_by('price')


# ==========================================
# Schema: Slice products by position
# ==========================================
class ProductOutSlice(Schema):
	id: int
	name: str
	slug: str
	is_digital: bool
	is_active: bool
	price: float

@router.get(
	'/products/q/slice-range',
	tags=['module6'],
	summary = 'Return products by slice range [start:end]',
	response = List[ProductOutSlice]
)
def get_products_by_slice_range(
	request,
	start: int = Query(0, ge=0, description='Start index (inclusive)'),
	end: int = Query(10, gt=0, description='End index (exclusive)'),
	active_only: Optional[bool] = Query(None, description='Filter only active products if True'),
):
	filters = Q()

	if active_only:
		filters &= Q(is_active=True)

	return Product.objects.filter(filters).order_by('id')[start:end]

#endregion CATEGORY



#region CHALLENGES

# ==========================================
# Task: Retrieve the First and Last Product Entries
# Filter[1]: Active products only
# Order By: id
# Fields: All Fields
# Extra[1]: Should not return duplicate records.
# ==========================================
def first_approach():
	queryset = Product.objects.active().order_by('id')
	total = queryset.count()

	first_five = list(queryset[:5])
	last_five = list(queryset[max(total - 5, 0):])

	# Make sure no duplicate included
	products = list({p.id: p for p in first_five + last_five}.values())
	return products


def second_approach():
	first_five = Product.objects.active().order_by('id')[:5]
	last_five = Product.objects.active().order_by('-id')[:5]

	combined = list( {p.id: p for p in list(first_five) + list(last_five)}.values() )

	# Sort the result by ID (ASC)
	products = sorted(combined, key=lambda p: p.id)

	return products



class ProductOut(Schema):
	id: int
	name: str
	slug: str
	is_digital: bool
	is_active: bool
	price: float

@router.get(
	'/products/get-5-fl',
	tags=['Challenge_6'],
	summary='Get the First and Last 5 Added Products',
	response=List[ProductOut]
)
def get_5_first_last_products(request):
	# products = first_approach()
	products = second_approach()

	return products


# ==========================================
# Task: Retrieve Orders from the last 30 days
# Return: ALl Fields
# ==========================================
class OrderOut(Schema):
	created: datetime


@router.get(
	'/orders/get-30',
	tags=['Challenge_6'],
	summary='Get Orders From the Last 30 Days',
	response=List[OrderOut]
)
def get_order_30(request):
	thirty_days_ago = now() - timedelta(days=30)	# Calculate 30 days ago

	orders = Order.objects.filter(created_at__gte=thirty_days_ago)

	return orders

	

#endregion CHALLENGES