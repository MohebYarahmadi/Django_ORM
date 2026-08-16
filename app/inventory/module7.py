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

#endregion START