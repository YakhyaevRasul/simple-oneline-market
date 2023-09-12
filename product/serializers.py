from rest_framework import serializers
from rest_framework.validators import ValidationError
import requests
from product import models


class CallBackRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CallBackRequest
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"


class ProductCommentGetSerializer(serializers.ModelSerializer):
    commentor = serializers.CharField(source="user.full_name")

    class Meta:
        fields = ("commentor", "comment", "created_at")
        model = models.ProductComment


class ProductSerializer(serializers.ModelSerializer):
    comments = ProductCommentGetSerializer(many=True, read_only=True)
    ratings = serializers.SerializerMethodField(read_only=True)
    category = CategorySerializer()
    brand = BrandSerializer()
    images = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = "__all__"

    def get_ratings(self, obj):
        if not obj.ratings.exists():
            return 0
        return sum(rating.rating for rating in obj.ratings.all()) / obj.ratings.count()

    def get_is_liked(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return obj in user.liked_products.all()

    def get_images(self, obj):
        request = self.context["request"]
        return [
            request.build_absolute_uri(photo.photo.url) for photo in obj.images.all()
        ]


class BasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "product", "count")
        model = models.BasketItem

    def create(self, validated_data):
        try:
            basket, create = models.Basket.objects.get_or_create(
                user=self.context["request"].user
            )
            item = models.BasketItem.objects.create(**validated_data, basket=basket)
        except:
            raise ValidationError("Product is in basket already")
        return item


class BasketItemGetSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    def get_product(self, obj):
        serializer_context = {"request": self.context["request"]}
        return ProductSerializer(obj.product, context=serializer_context).data

    class Meta:
        fields = ("id", "product", "count")
        model = models.BasketItem


class BasketSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    overall_cost = serializers.SerializerMethodField(read_only=True)
    overall_num_of_products = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Basket
        fields = ("id", "items", "overall_cost", "overall_num_of_products")

    def get_items(self, obj):
        serializer_context = {"request": self.context["request"]}
        return BasketItemGetSerializer(
            obj.items.all(), many=True, context=serializer_context
        ).data

    def get_overall_cost(self, obj):
        return sum(item.product.price * item.count for item in obj.items.all())

    def get_overall_num_of_products(self, obj):
        return sum(item.count for item in obj.items.all())


class OrderSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    items = BasketItemGetSerializer(many=True, read_only=True)
    overall_cost = serializers.SerializerMethodField(read_only=True)
    overall_num_of_products = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Order
        fields = (
            "id",
            "items",
            "name",
            "phone_number",
            "address",
            "overall_cost",
            "overall_num_of_products",
        )

    def send_to_telegram_group(self, order):
        URL = "https://api.telegram.org/bot5268448630:AAFJi6oSD5aasFUEQo0NpGuVwqt_FQT2N8c/sendMessage"
        order_info = f"Ismi: <b>{order.name}</b>\nTelefon: <b>{order.phone_number}</b>\nAdresi: <b>{order.address}</b>\n"
        i = 1
        total_cost = sum(item.product.price * item.count for item in order.items.all())
        for item in order.items.all():
            order_info += f"<b>{i}. {item.product.name}:</b> {item.product.price} x {item.count} = {item.product.price*item.count},\n"
            i += 1
        payload = {
            "chat_id": "-746869289",
            "text": "Yangi buyurtma:\n\n" + order_info + f"Jami: {total_cost}",
            "parse_mode": "HTML",
        }
        res = requests.post(URL, payload)

    def create(self, validated_data):
        user = self.context["request"].user
        basket, _ = models.Basket.objects.get_or_create(user=user)
        if not basket.items.exists():
            raise ValidationError("You don't have any item in your basket")
        order = models.Order.objects.create(**validated_data, user=user)
        for item in user.basket.items.all():
            item.order = order
            item.basket = None
            item.save()
        self.send_to_telegram_group(order)
        return order

    def get_overall_cost(self, obj):
        return sum(item.product.price * item.count for item in obj.items.all())

    def get_overall_num_of_products(self, obj):
        return sum(item.count for item in obj.items.all())


class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "product", "comment")
        model = models.ProductComment

    def create(self, validated_data):
        comment = models.ProductComment.objects.create(
            **validated_data, user=self.context["request"].user
        )
        return comment


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "product", "rating")
        model = models.ProductRating

    def create(self, validated_data):
        try:
            rating = models.ProductRating.objects.create(
                **validated_data, user=self.context["request"].user
            )
        except:
            raise ValidationError(
                "You have already rated this product you can change that rating now"
            )
        return rating
