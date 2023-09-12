import requests
from django.db.models import Q
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.validators import ValidationError
from django_filters import rest_framework as filters

from product.filters import ProductFilter
from product.paginations import DefaultLimitOffSetPagination
from product.models import (
    Product,
    Brand,
    Category,
    Basket,
    BasketItem,
    Order,
    ProductComment,
    ProductRating,
    CallBackRequest,
)
from product.serializers import (
    CallBackRequestSerializer,
    ProductCommentSerializer,
    BasketItemGetSerializer,
    ProductRatingSerializer,
    BasketItemSerializer,
    CategorySerializer,
    ProductSerializer,
    BasketSerializer,
    OrderSerializer,
    BrandSerializer,
)


class CallBackRequestView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = CallBackRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.validated_data
        URL = "https://api.telegram.org/bot5268448630:AAFJi6oSD5aasFUEQo0NpGuVwqt_FQT2N8c/sendMessage"
        payload = {
            "chat_id": "-746869289",
            "text": "Yangi chaqiruv:\n"
            + "telefon: "
            + data["phone"]
            + "\n"
            + "Ismi: "
            + data["name"]
            + "\n"
            + "Viloyati: "
            + data["region"]
            + "\n",
        }
        requests.post(URL, payload)

        return Response({"message": "accepted"}, status=status.HTTP_201_CREATED)


class BrandModelViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = IsAdminUser

    def get_permissions(self):
        if self.request.method in ["GET", "LIST", "RETREIVE"]:
            permission_classes = [
                AllowAny,
            ]
        else:
            permission_classes = [
                IsAdminUser,
            ]
        return [perm() for perm in permission_classes]

    # def get_queryset(self):
    #     is_famous = self.request.query_params.get('is_famous', None)
    #     if is_famous:
    #         return self.queryset.filter(is_famous=True)
    #     return self.queryset


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = IsAdminUser

    def get_permissions(self):
        if self.request.method in ["GET", "LIST", "RETREIVE"]:
            permission_classes = [
                AllowAny,
            ]
        else:
            permission_classes = [
                IsAdminUser,
            ]
        return [perm() for perm in permission_classes]

    # def get_queryset(self):
    #     is_main = self.request.query_params.get('is_main')
    #     if is_main:
    #         return self.queryset.filter(is_main=True)
    #     return self.queryset


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = IsAdminUser
    pagination_class = DefaultLimitOffSetPagination
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter
    authentication_classes = ()

    def get_permissions(self):
        if self.request.method in ["GET", "LIST", "RETREIVE"]:
            permission_classes = [
                AllowAny,
            ]
        else:
            permission_classes = [
                IsAdminUser,
            ]
        return [perm() for perm in permission_classes]


class BasketModelViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = (IsAuthenticated,)
    allowed_methods = ["list"]

    def list(self, request, *args, **kwargs):
        try:
            basket = request.user.basket
        except:
            Basket.objects.create(user=request.user)
        return Response(
            {
                "basket": self.serializer_class(
                    request.user.basket, context={"request": self.request}
                ).data
            },
            status=status.HTTP_200_OK,
        )

    def get_serializer_context(self):
        context = super(OrderModelViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class BasketItemModelViewSet(ModelViewSet):
    queryset = BasketItem.objects.all()
    serializer_class = BasketItemSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return self.queryset.filter(basket=self.request.user.basket)

    def get_serializer_context(self):
        context = super(BasketItemModelViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class OrderModelViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    pagination_class = DefaultLimitOffSetPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super(OrderModelViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class ProductCommentModelViewSet(ModelViewSet):
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    pagination_class = DefaultLimitOffSetPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super(ProductCommentModelViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class ProductRatingModelViewSet(ModelViewSet):
    queryset = ProductRating.objects.all()
    serializer_class = ProductRatingSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    pagination_class = DefaultLimitOffSetPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super(ProductRatingModelViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context
