from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from user.models import User
from user.serializers import UserLoginSerializer
from user.utils import get_formatted_phone_number


class MyTokenObtainPairView(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ['post']

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = get_formatted_phone_number(request.data['phone_number'])
        user = None
        try:
            user = User.objects.get(phone_number=phone_number)
        except:
            raise ValidationError("User was not found")
        if not user.check_password(request.data['password']):
            return Response({'message':'password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
