from typing import Optional, List
from django.db.models import Q
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




#endregion