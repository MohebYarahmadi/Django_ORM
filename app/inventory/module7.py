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

#region START
# =====================================
# Product + Category: Return product and category info by product IDs
# =====================================
class CategoryNested(Schema):
	id: int
	name: str
	slug: str
	level: int
	is_active: bool

class ProductWithCategoryOut(Schema):
	id: int
	name: str
	slug: str
	price: float
	is_active: bool
	category: CategoryNested

@router.get(
	'/products/by-id/',
	tags=['modlue7'],
	summary='Return product and category info by product ids',
	response=list[ProductWithCategoryOut]
)
def get_products_by_id(request, ids: List[int] = Query(...)):
	qs = Product.objects.select_related('category').filter(id__in=ids)
	return qs

#endregion START