from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.timezone import datetime
from customer.models import OrderModel
from django.contrib.admin.views.decorators import staff_member_required
from django.views import View
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import StaffRegistrationForm
from django.db.models import Sum

@method_decorator(staff_member_required, name='dispatch')
class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        # get the current date
        today = datetime.today()
        orders = OrderModel.objects.filter(
            created_on__year=today.year, created_on__month=today.month, created_on__day=today.day)
        

        # loop through the orders and add the price value, check if order is not shipped
        unshipped_orders = []
        total_revenue = 0
        for order in orders:
            total_revenue += order.price

            if order.is_shipped==False:
                unshipped_orders.append(order)

        # pass total number of orders and total revenue into template
        context = {
            'orders': unshipped_orders,
            'total_revenue': total_revenue,
            'today_orders_count': orders.count()
        }

        return render(request, 'restaurant/dashboard.html', context)
        

@method_decorator(staff_member_required, name='dispatch')
class OrderDetails(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        context = {
            'order': order
        }
        return render(request, 'restaurant/order_details.html', context)

    def post(self, request, pk, *args, **kwargs):
        
            order = OrderModel.objects.get( pk=pk)
            order.is_shipped = True
            order.save()

            context = {
                'order': order,
                'success_message': 'Order status updated successfully'
            }
            return render(request, 'restaurant/order_details.html', context)
        
            
class StaffRegistrationView(View):
    def get(self, request, *args, **kwargs):
        form = StaffRegistrationForm()
        return render(request, 'restaurant/staff-registration.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff account created successfully!')
            return redirect('dashboard')
        return render(request, 'restaurant/staff-registration.html', {'form': form})