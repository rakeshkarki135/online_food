from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


# Create your models here.

class CarouselItems(models.Model):
     image =  models.ImageField(upload_to='carousel/%y/%m%d') 
     first_title = models.CharField(max_length=100)
     span_title =models.CharField(max_length=100)
     last_title = models.CharField(max_length=100)
     text = models.TextField()
     
     class Meta:
          verbose_name_plural = 'Carousel Table' 
          
          
class Contact(models.Model):
     name = models.CharField(max_length=200)
     email = models.EmailField()
     subject = models.CharField(max_length=200)
     message = models.TextField()
     added_on = models.DateField(auto_now_add=True)
     is_approved = models.BooleanField(default=True)
     
     def __str__(self):
          return self.name
     
     class Meta:
          verbose_name_plural = "Contact Table"
     
class Category(models.Model):
     name = models.CharField(max_length=100 , unique=True , blank=False , null=False)
     image = models.ImageField(upload_to='categories/%y/%m/%d')  
     icon = models.CharField(max_length=50 , blank=True)
     description = models.TextField()
     added_on = models.DateTimeField(auto_now_add=True)
     updated_on = models.DateTimeField(auto_now=True)  
     
     def __str__(self):
          return self.name
     
     class Meta:
          verbose_name_plural = 'Category Table'
          
           
class Dish(models.Model):
     name = models.CharField(max_length=200 , unique=True)
     image = models.ImageField(upload_to='dishes/%y/%m/%d')
     ingredients =  models.TextField()
     details = models.TextField(blank=True)
     category = models.ForeignKey(Category , on_delete=models.CASCADE)
     price = models.FloatField()
     discount_price = models.FloatField(blank=True)
     is_available = models.BooleanField(blank=True)
     added_on = models.DateTimeField(auto_now_add=True) 
     updated_on = models.DateTimeField(auto_now=True)
     
     def __str__(self):
          return self.name
     
     class Meta:
          verbose_name_plural="Dish Table"
          
          
class Profile(models.Model):
     user = models.OneToOneField(User,on_delete=models.CASCADE)
     profile_pic = models.ImageField(upload_to="media/",null=True,blank=True)
     contact_number = models.CharField(max_length=20,null=True,blank=True)
     address = models.TextField(blank=True)
     updated_on = models.DateTimeField(auto_now=True)
     
     def __str__(self):
          # getting the name from user 
          return self.user.first_name
     
     def get_cart_count(self):
          # counting the logged in user unpaid item
          return CartItems.objects.filter(cart__is_paid=False ,cart__user=self.user).count()
     
     def get_order_count(self):
          user = self.user
          try:
               cart=Cart.objects.get(user=user , is_paid=False)
               return Order.objects.filter(user=user , cart=cart).count()
          
          except Cart.DoesNotExist:
               return 0
               
     class Meta:
          # setting the main table name  
          verbose_name_plural = " Profile Table "


          
class Cart(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
     is_paid = models.BooleanField(default=False) 

     
     def __str__(self):
          return self.user.first_name
     
     def calculate_total_price(self):
          total_price = Decimal('0.00')
          cart_items = self.cart_items.all()
          for cart_item in cart_items:
               total_price += cart_item.get_product_price()
               
          return total_price
          
     # def get_cart_total(self):
     #      cart_items = self.cart_items.all()
     #      price=[]
     #      for cart_item in cart_items:
     #           price.append(cart_item.dish.price)
     #      return sum(price)
     
ORDER_STATUS = (
     ("Order Received" , "Order Received"),
     ("Order Processing" , "Order Processing"),
     ("Order Completed" , "Order Completed"),
     ("Order Cancelled" , "Order Cancelled")
)

METHOD = (
     ("Cash On Delivery" ,"Cash On Delivery"),
     # ("Khalti" , "Khalti"),
     )
     
class Order(models.Model):
     user = models.ForeignKey(User , on_delete=models.CASCADE , null=True , default=None)
     cart = models.ForeignKey(Cart , on_delete=models.SET_NULL , null=True , default=None)
     ordered_by = models.CharField(max_length=200)
     shipping_address = models.CharField(max_length=200)
     mobile = models.IntegerField(null=True)
     email = models.EmailField(null=True , blank=True)
     total = models.PositiveIntegerField()
     order_status = models.CharField(max_length=50 , choices=ORDER_STATUS)
     ordered_on = models.DateTimeField(auto_now=True)
     # payment_method = models.CharField(max_length=20 , choices=METHOD, null=True , default= "Cash On Delivery")
     payment_method = models.CharField(max_length=20 ,  null=True , default= "Cash On Delivery")
     payment_completed = models.BooleanField(default=False , null= True , blank= True)
     
     def __str__(self):
          return self.user.first_name
      
     class Meta:
          verbose_name_plural = "Order Table"
          
class CartItems(models.Model):
     cart = models.ForeignKey(Cart , on_delete=models.CASCADE , related_name='cart_items')
     dish = models.ForeignKey(Dish , on_delete=models.SET_NULL, null=True, blank=True )
     quantity = models.PositiveIntegerField(default=1)
     
     def __str__(self):
          return f"{self.cart.user.first_name}__{self.quantity}*{self.dish.name}"
     
     def get_product_price(self):
          return Decimal(str(self.dish.discount_price)) * Decimal(self.quantity)
     
     