from rest_framework.routers import SimpleRouter
from django.urls import path

from user.views import (
    DistrictModelViewSet,
    LikedProductAPIView,
    RegionModelViewSet,
    UserModelViewSet,
    UserCodeSendView,
    UserRegisterView,
    UserProfileView,
)

router = SimpleRouter()
router.register("regions", RegionModelViewSet)
router.register("districts", DistrictModelViewSet)
router.register("users", UserModelViewSet)

urlpatterns = [
    path("liked-products/", LikedProductAPIView.as_view()),
    path("send-code/", UserCodeSendView.as_view()),
    path("user-register/", UserRegisterView.as_view()),
    path("user-profile/", UserProfileView.as_view()),
]

urlpatterns += router.urls
