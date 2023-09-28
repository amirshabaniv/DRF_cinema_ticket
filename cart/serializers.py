from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem, Coupon
from cinema.serializers import PlayTimeSerializer
from cinema.models import PlayTime
from django.db import transaction


class CartItemSerializer(serializers.ModelSerializer):
    playtime = PlayTimeSerializer()
    sub_total = serializers.SerializerMethodField(method_name='total')

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'quantity', 'playtime', 'sub_total']

    def total(self, cartitem:CartItem):
        return cartitem.quantity * cartitem.playtime.ticket_price


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    grand_total = serializers.SerializerMethodField(method_name='main_total') 

    class Meta:
        model = Cart
        fields = ['id', 'items', 'grand_total']
        extra_kwargs = {
            'id' : {'read_only':True},
        }
    
    def main_total(self, cart: Cart):
        items = cart.items.all()
        total = sum([item.quantity * item.playtime.ticket_price for item in items])
        return total


class AddCartItemSerializer(serializers.ModelSerializer):
    playtime_id = serializers.IntegerField()
    
    def validate_playtime_id(self, value):
        if not PlayTime.objects.filter(pk=value).exists():
            raise serializers.ValidationError("There is no product associated with the given ID")
        
        return value
    
    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        playtime_id = self.validated_data["playtime_id"] 
        quantity = self.validated_data["quantity"]
        
        try:
            cartitem = CartItem.objects.get(playtime_id=playtime_id, cart_id=cart_id)
            cartitem.quantity += quantity
            cartitem.save()
            self.instance = cartitem

        except:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
            
        return self.instance
         

    class Meta:
        model = CartItem
        fields = ["id", "playtime_id", "quantity"]


class UpdateCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ['id', "quantity"]
        extra_kwargs = {
            'id' : {'read_only':True},
        }


class OrderItemSerializer(serializers.ModelSerializer):
    playtime = PlayTimeSerializer()
    get_item_cost = serializers.SerializerMethodField(method_name='get_cost')

    class Meta:
        model = OrderItem
        fields = ['id', 'playtime', 'quantity', 'get_item_cost']
    
    def get_cost(self, orderitem:OrderItem):
        return orderitem.playtime.ticket_price * orderitem.quantity


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    get_total_price = serializers.SerializerMethodField(method_name='get_t_price')

    class Meta:
        model = Order
        fields = ['id', 'placed_at', 'pending_status', 'owner', 'discount', 'items', 'get_total_price']

    def get_t_price(self, order:Order):
        items = order.items.all()
        total = sum([item.quantity * item.playtime.ticket_price for item in items])
        if order.discount:
            discount_price = (order.discount / 100) * total
            return int(total - discount_price)
        return total


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()
    
    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError("This cart_id is invalid")
        
        elif not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError("Sorry your cart is empty")
        
        return cart_id
    
    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data["cart_id"]
            user_id = self.context["user_id"]
            order = Order.objects.create(owner_id = user_id)
            cartitems = CartItem.objects.filter(cart_id=cart_id)
            orderitems = [
                OrderItem(order=order, 
                    playtime=item.playtime, 
                    quantity=item.quantity
                    )
            for item in cartitems
            ]
            OrderItem.objects.bulk_create(orderitems)
            Cart.objects.filter(id=cart_id).delete()
            return order 


class UpdateOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order 
        fields = ["pending_status"]

