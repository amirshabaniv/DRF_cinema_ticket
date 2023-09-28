from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, Coupon

admin.site.register(Cart)

@admin.register(CartItem)
class CartItemsAdmin(admin.ModelAdmin):
    list_display = ['cart']

admin.site.register(Order)

admin.site.register(OrderItem)

admin.site.register(Coupon)
