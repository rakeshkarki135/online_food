from django.contrib import admin
from .models import *

# change header name
admin.site.site_header = "FoodZone | Admin"

# to display in tabular form in admin panel
class ContactAdmin(admin.ModelAdmin):
     list_display=('id','name','email','subject', 'added_on' ,'message')
admin.site.register(Contact , ContactAdmin)

class CategoryAdmin(admin.ModelAdmin):
     list_display=('id','name','added_on','updated_on')
admin.site.register(Category,CategoryAdmin)

class DishAdmin(admin.ModelAdmin):
     list_display=('id','name','price','added_on','updated_on')
admin.site.register(Dish,DishAdmin)

admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(CarouselItems)
admin.site.register(Cart)
admin.site.register(CartItems)
