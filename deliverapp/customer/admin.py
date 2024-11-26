from django.contrib import admin
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MenuItem, Category, OrderModel



admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(OrderModel)