from django.contrib import admin

from product import models


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


class ImageInline(admin.TabularInline):
    model = models.ProductImage


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ]
    list_display = ['id', 'name', 'category', 'brand', 'price']
    search_fields = ['name', 'category__name', 'brand__name']


class BasketItemInline(admin.TabularInline):
    model = models.BasketItem
    fields = ['product', 'count']
    extra = 0

@admin.register(models.Basket)
class BasketAdmin(admin.ModelAdmin):
    inlines = [BasketItemInline,]
    
    
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'address', 'created_at', 'updated_at']
    search_fields = ['user__firstname', 'user__lastname']
    inlines = [BasketItemInline]


@admin.register(models.ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment', 'product']


@admin.register(models.ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'product']
