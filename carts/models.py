from django.db import models
from store.models import Product, Variation
from base.models import User

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.cart_id
    
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    variation = models.ManyToManyField(Variation, blank=True, related_name='variation')
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    
    def __str__(self):
        return self.product.product_name
    
    def get_amount(self):
        return int(self.product.price) * int(self.quantity)
    
    # class Meta:
    #     verbose_name = 'Cart Item'
    
    