from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views
from django.urls import path, include


router = routers.DefaultRouter()

router.register('carts', views.CartViewSet)
router.register('orders', views.OrderViewSet, basename='orders')

cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_router.register("cartitems", views.CartItemViewSet, basename="cart-items")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(cart_router.urls)),
]