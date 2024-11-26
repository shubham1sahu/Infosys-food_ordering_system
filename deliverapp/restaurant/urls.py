from django.urls import path
from .views import Dashboard, OrderDetails, StaffRegistrationView

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('orderdetails/<int:pk>/', OrderDetails.as_view(), name='order_details'),
    
    path('staff-registration/', StaffRegistrationView.as_view(), name='staff-registration'),
]