from decimal import Decimal, ROUND_DOWN
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http.response import JsonResponse
from django.shortcuts import redirect
# Import models
from .models import UserPoint, PointsSetting
from applications.cart.models import Cart
# Import function
from applications.cart.shopping_cart import calculate_cart

# Create your views here.
class PointsView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user_app:user_login')

    def get(self, request, *args, **kwargs):
        points = kwargs['points']
        if isinstance(points, int):
            points_setting = PointsSetting.objects.get_point_setting()
            if points >= points_setting.redemption_rate:
                # We update the cart with the discount
                cart = Cart.objects.filter(id_user=request.user.id).first()
                user_points = UserPoint.objects.get_user_points(request.user.id)
                discount = Decimal(points / points_setting.redemption_rate)
                discount = discount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                cart.discount = discount
                calculate_cart(cart)
                # We subtract and update the user's points
        return JsonResponse({'discount': cart.discount, 'total': cart.total, 'user_points': user_points.points})
    

class RemoveDiscountView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user_app:user_login')

    def get(self, request, *args, **kwargs):
        user_points = UserPoint.objects.get_user_points(request.user.id)
        cart = Cart.objects.filter(id_user=request.user.id).first()
        # we remove the discount from the cart
        cart.total += cart.discount
        cart.discount = 0.00
        calculate_cart(cart)
        if kwargs['page'] == 'checkout':
            return JsonResponse({'total': cart.total, 'user_points': user_points.points})
        elif kwargs['page'] == 'cart':
            return redirect('cart_app:cart')