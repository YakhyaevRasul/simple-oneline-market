from django.core.validators import RegexValidator
from rest_framework import serializers
from user.utils import pattern

from user.models import User, Region, District


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"


class ProductLikedSerializer(serializers.Serializer):
    product_id = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(read_only=True, source="region.name")
    district_name = serializers.CharField(read_only=True, source="district.name")
    # avatar_url = serializers.SerializerMethodField(read_only=True)

    # def get_avatar_url(self, usr):
    #     request = self.context.get('request')
    #     avatar_url = usr.avatar.url
    #     return request.build_absolute_uri(avatar_url)

    class Meta:
        model = User
        fields = [
            "phone_number",
            "firstname",
            "lastname",
            "region",
            "avatar",
            "bonus",
            "region_name",
            "district",
            "district_name",
            "is_active",
        ]
        read_only_fields = ("phone_number", "bonus")


class UserRegisterSerializer(serializers.ModelSerializer):
    code_regex = RegexValidator(regex=r"^\d{6}$", message="123456 holatda kiriting")
    code = serializers.CharField(max_length=6, validators=[code_regex])
    phone_regex = RegexValidator(regex=pattern, message="998901234567 holatda kiriting")
    phone_number = serializers.CharField(required=True, validators=[phone_regex])

    class Meta:
        model = User
        fields = ["id", "phone_number", "firstname", "lastname", "code", "password", "region", "district"]
        read_only_fields = ("id",)
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
                "style": {"input_type": "password"},
            }
        }


class UserCodeSendSerializer(serializers.Serializer):
    phone_regex = RegexValidator(regex=pattern, message="998901234567 holatda kiriting")
    phone_number = serializers.CharField(required=True, validators=[phone_regex])


class UserLoginSerializer(serializers.Serializer):
    phone_regex = RegexValidator(regex=pattern, message="998901234567 holatda kiriting")
    phone_number = serializers.CharField(required=True, validators=[phone_regex])
    password = serializers.CharField(required=True)
