from django.urls import path
from rest_framework.routers import SimpleRouter

from product import views

router = SimpleRouter()
router.register('brands', views.BrandModelViewSet)
router.register('categories', views.CategoryModelViewSet)
router.register('products', views.ProductModelViewSet)
router.register('basket', views.BasketModelViewSet)
router.register('basket-items', views.BasketItemModelViewSet)
router.register('orders', views.OrderModelViewSet)
router.register('product-comments', views.ProductCommentModelViewSet)
router.register('product-ratings', views.ProductRatingModelViewSet)

urlpatterns = router.urls
urlpatterns += [
    path('call-back-requests/', views.CallBackRequestView.as_view()),
]
