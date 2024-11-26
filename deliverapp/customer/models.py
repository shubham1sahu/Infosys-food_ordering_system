from django.db import models


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ManyToManyField('Category', related_name='item')

    def __str__(self):
        return self.name



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField(
        'MenuItem', related_name='order', blank=True)
    name=models.CharField(max_length=50, blank=True)

    def update_price(self):
        self.price = sum(item.price for item in self.items.all())
        self.save()

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = 0
        super().save(*args, **kwargs)
        
    email=models.CharField(max_length=40,blank=True)
    street=models.CharField(max_length=50,blank=True)
    city=models.CharField(max_length=50,blank=True)
    state=models.CharField(max_length=50,blank=True)
    pin=models.CharField(max_length=20,blank=True)
    is_paid = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=50, default='PENDING')
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'