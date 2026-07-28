from ninja import NinjaAPI

from .module4 import router as router4

api = NinjaAPI(
	title='Django ORM Mastery API',
	description='Endpoints for managing products, promotions and orders',
	version='1.0.0'
)


# Register route
api.add_router("mod4/", router4)