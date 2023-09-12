import os
from uuid import uuid4
from django.db import models
from django.contrib.postgres.fields import ArrayField

def user_avatar_file_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("users-avatars/", filename)


def product_image_file_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("products-images/", filename)


def category_image_file_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("categores-images/", filename)


def brand_image_file_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("categores-images/", filename)


class CallBackRequest(models.Model):
    name = models.CharField(max_length=127)
    region = models.CharField(max_length=127)
    phone = models.CharField(max_length=32)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=127)
    image = models.FileField(upload_to=category_image_file_path, null=True, blank=True)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=127)
    image = models.FileField(upload_to=brand_image_file_path, null=True, blank=True)
    is_famous = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0)
    description =ArrayField(models.CharField(max_length=256),null=True, blank=True)
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
        blank=True,
    )
    brand = models.ForeignKey(
        "Brand", on_delete=models.SET_NULL, 
        related_name="products", null=True, blank=True
    )
    is_famous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    photo = models.FileField(
        default="media/default-photo.jpg", upload_to=product_image_file_path
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )


class ProductComment(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="comments"
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[:20]


class ProductRating(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="ratings"
    )
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="product_ratings"
    )
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "user")

    def __str__(self):
        return self.product.name + "rating: " + str(self.rating)


class Basket(models.Model):
    user = models.OneToOneField(
        "user.User", on_delete=models.CASCADE, related_name="basket"
    )

    def __str__(self):
        return self.user.full_name() + "'s basket"


class BasketItem(models.Model):
    basket = models.ForeignKey(
        "Basket", on_delete=models.SET_NULL, related_name="items", null=True, blank=True
    )
    order = models.ForeignKey(
        "Order", on_delete=models.SET_NULL, related_name="items", null=True, blank=True
    )
    product = models.ForeignKey("Product", on_delete=models.DO_NOTHING)
    count = models.IntegerField(default=1)

    class Meta:
        unique_together = ("product", "basket")
        ordering = ("-id",)

    def __str__(self):
        return self.product.name + " in basket"


class Order(models.Model):
    user = models.ForeignKey(
        "user.User", on_delete=models.PROTECT, related_name="orders"
    )
    name = models.CharField(max_length=128, null=True, blank=True)
    phone_number = models.CharField(max_length=128, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.full_name() + "'s order on " + str(self.created_at)
