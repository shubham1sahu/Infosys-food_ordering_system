from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.About.as_view(), name='about'),
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Registration.as_view(), name='register'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('order/', views.Order.as_view(), name='order'),
    path('order-confirmation/<int:pk>', views.OrderConfirmation.as_view(), name='order-confirmation'),
    path('payment-confirmation/', views.OrderPayConfirmation.as_view(), name='payment-confirmation'),
   
    
   
]
