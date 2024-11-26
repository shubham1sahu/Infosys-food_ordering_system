from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.views import View
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import MenuItem, Category, OrderModel
from .forms import UserRegistrationForm, LoginForm


class Home(View):
    def get(self, request, *args, **kwargs):
        # Get menu categories for the home page
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'customer/home.html', context)


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')

class Login(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'customer/login.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                user_type = request.POST.get('user_type')
                if user_type == 'staff':
                    if user.is_staff:
                        messages.success(request, 'Staff login successful!')
                        return redirect('dashboard')
                    else:
                        messages.error(request, "You don't have staff permissions.")
                        return redirect('login')
                else:
                    messages.success(request, 'Login successful!')
                    return redirect('h')
            else:
                messages.error(request, 'Invalid username or password')
        return render(request, 'customer/login.html', {'form': form})
    
class Registration(View):
    def get(self, request, *args, **kwargs):
        form = UserRegistrationForm()
        return render(request, 'customer/registration.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Welcome! Your registration was successful!')
                return redirect('index')
            except Exception as e:
                print(f"Registration error: {str(e)}")  # For debugging
                messages.error(request, 'Registration failed. Please try again.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
        
        return render(request, 'customer/registration.html', {'form': form})




class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        appetizers = MenuItem.objects.filter(
            category__name__contains='Appetizer')
        entres = MenuItem.objects.filter(category__name__contains='Entre')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        # pass into context
        context = {
            'appetizers': appetizers,
            'entres': entres,
            'desserts': desserts,
            'drinks': drinks,
        }

        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name=request.POST.get('name')
        email=request.POST.get('email')
        street=request.POST.get('street')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pin=request.POST.get('pin')
        
        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            pin=pin
            
            
            )
        order.items.add(*item_ids)
        body=('Thank ypu for your order! Your foood is being made and will be delivered soon!\n'
              f'Your total :{price}\n'
              'Thank you again for your order!')

        send_mail(
            'Thanks You For Your Order !',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )



        context = {
            'items': order_items['items'],
            'price': price,
        }
        return redirect('order-confirmation',pk=order.pk)

        
@method_decorator(csrf_exempt, name='dispatch')
class OrderConfirmation(View):
    def get(self, request,pk,*args,**kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': '{:.2f}'.format(float(order.price)),
            'paypal_client_id': settings.PAYPAL_CLIENT_ID,
        }
        return render(request, 'customer/order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        try:
            data = json.loads(request.body)
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')
    
class H(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/h.html')
    

class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect('login')

