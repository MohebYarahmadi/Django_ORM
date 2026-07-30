from django.contrib import admin

from .models import (
	Category, Product, Order, OrderProduct,
	ProductPromotionEvent, PromotionEvent,
	StockManagement, User
)

# Register your models here.
# admin.site.register(Category)
# admin.site.register(Product)
# admin.site.register(Order)
# admin.site.register(OrderProduct)
# admin.site.register(ProductPromotionEvent)
# admin.site.register(PromotionEvent)
# admin.site.register(StockManagement)
# admin.site.register(User)

# Inline for Order Products in OrderAdmin
class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    fields = ("product", "quantity")
    autocomplete_fields = ["product"]


# Inline for linking Products to Promotion Events
class ProductPromotionEventInline(admin.TabularInline):
    model = ProductPromotionEvent
    extra = 0
    autocomplete_fields = ["product", "promotion_event"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "parent", "is_active", "level"]
    search_fields = ["name"]
    list_filter = ["is_active", "level"]
    ordering = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "category", "price", "is_active", "is_digital"]
    search_fields = ["name", "slug"]
    list_filter = ["is_active", "is_digital", "category"]
    autocomplete_fields = ["category"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["name"]


@admin.register(PromotionEvent)
class PromotionEventAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "end_date", "price_reduction"]
    search_fields = ["name"]
    ordering = ["-start_date"]
    inlines = [ProductPromotionEventInline]


@admin.register(StockManagement)
class StockManagementAdmin(admin.ModelAdmin):
    list_display = ["product", "quantity", "last_checked_at"]
    autocomplete_fields = ["product"]
    readonly_fields = ["last_checked_at"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email"]
    search_fields = ["username", "email"]
    ordering = ["username"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_at", "updated_at"]
    search_fields = ["user__username", "id"]
    ordering = ["-created_at"]
    inlines = [OrderProductInline]


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "quantity"]
    autocomplete_fields = ["order", "product"]


@admin.register(ProductPromotionEvent)
class ProductPromotionEventAdmin(admin.ModelAdmin):
    list_display = ["product", "promotion_event"]
    autocomplete_fields = ["product", "promotion_event"]
