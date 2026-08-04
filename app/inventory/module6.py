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


#endregion