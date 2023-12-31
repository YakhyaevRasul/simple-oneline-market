from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import logout
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import CreateAPIView
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.validators import ValidationError
from user.utils import (
    send_code_to_phone,
    validate_phone_number,
    get_formatted_phone_number,
)
from user.filters import DistrictFilter
from product.models import Product
from user.serializers import (
    UserRegisterSerializer,
    UserCodeSendSerializer,
    UserProfileSerializer,
    RegionSerializer,
    DistrictSerializer,
    ProductLikedSerializer,
)
from product.paginations import DefaultLimitOffSetPagination
from product.serializers import ProductSerializer
from user.models import VerificationCode, User, Region, District


class RegionModelViewSet(ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
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


class LikedProductAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(responses={200: ProductSerializer(many=True)})
    def get(self, request):
        return Response(
            {"likeds": ProductSerializer(self.request.user.liked_products.all(), many=True, context={"request": request}).data}
        )
    @swagger_auto_schema(request_body=ProductLikedSerializer)
    def patch(self, request):
        product = Product.objects.get(id=request.data["productId"])
        user = request.user
        if product in user.liked_products.all():
            user.liked_products.remove(product)
            return Response(
                {"message": "product was removed from likeds"},
                status=status.HTTP_202_ACCEPTED,
            )
        user.liked_products.add(product)
        return Response(
            {"message": "product was added to likeds"},
            status=status.HTTP_202_ACCEPTED,
        )


class DistrictModelViewSet(ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = DistrictFilter
    pagination_class = DefaultLimitOffSetPagination

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


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        ### User will get his or her infos in this endpoint
        """
        return Response(
            UserProfileSerializer(request.user).data, status=status.HTTP_200_OK
        )

    def patch(self, request):
        serializer = UserProfileSerializer(
            instance=request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Ma'lumotlaringiz yangilandi", "user": serializer.data},
            status=status.HTTP_202_ACCEPTED,
        )

    # def get_serializer_context(self):
    #     context = super(User, self).get_serializer_context()
    #     context.update({"request": self.request})
    #     return context


class UserCodeSendView(APIView):
    http_method_names = ["post"]
    permission_classes = [AllowAny]

    def check_user_exists(self, phone_number):
        try:
            User.objects.get(phone_number=phone_number)
            raise ValidationError("User with this phone_number already exists")
        except:
            pass

    def post(self, request, *args, **kwargs):
        """
        ### endpoint where code is sent to given phone_number
            - need to provide with
        {
             "phone_number":"+998900087373"
        }
        """
        serializer = UserCodeSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        phone_number = data["phone_number"]
        phone_number = get_formatted_phone_number(phone_number)
        self.check_user_exists(phone_number)
        code = VerificationCode.objects.filter(
            expire_at__gte=timezone.now(), contact=phone_number
        ).first()
        if code is not None:
            return Response(
                "Maxfiy kod allaqachon yuborilgan, bir ozdan keyin urinib ko‘ring",
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            User.objects.get(phone_number=phone_number)
            return Response(
                {"message": "User already exists with this phone_number"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except:
            pass
        code = VerificationCode.objects.create(contact=phone_number)
        message = f"BitBad savdo portalida sizning maxfiy raqamingiz: {code.code}"
        # res = send_code_to_phone(code.code, "998"+phone_number, message)
        return Response(
            {"message": "Code was sent", "code": code.code}, status=status.HTTP_200_OK
        )


class UserRegisterView(CreateAPIView):
    """
    ### Endpoint where one is registered by giving infos below
    {
        "phone_number":"+998981234567",
        "code": "123456",    #sent to the phone number above with the /code-send api
        "password":"somethign"
    }
    """

    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        phone_number = data["phone_number"]
        print(phone_number)
        phone_number = get_formatted_phone_number(phone_number)
        code = VerificationCode.objects.filter(
            expire_at__gte=timezone.now(), contact=phone_number
        ).first()
        if code is None:
            return Response(
                "Maxfiy raqamni amal qilish muddati tugadi. Qayta jo‘nating",
                status=status.HTTP_400_BAD_REQUEST,
            )
        if code.code != data["code"]:
            return Response(
                "Siz kiritgan maxfiy raqam noto‘g‘ri",
                status=status.HTTP_400_BAD_REQUEST,
            )
        data.pop("code")
        password = data.pop("password")
        data["phone_number"] = phone_number
        print(data["phone_number"])
        user = User.objects.create(**data)
        user.set_password(password)
        user.save()
        code.delete()
        return Response(
            {"message": "User was created successfully"}, status=status.HTTP_201_CREATED
        )


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    pagination_class = DefaultLimitOffSetPagination
    permission_classes = (IsAdminUser)