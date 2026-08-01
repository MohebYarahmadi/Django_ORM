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

#endregion

