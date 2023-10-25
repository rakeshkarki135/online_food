from django.urls import path, include
from . import views 
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
     
     path('' , views.admin_login , name='admin_login'),
     path('admin_dashboard/' , views.admin_dashboard,name='admin_dashboard'),
     path('table/' , views.table , name='tables'),
     # admin panel items
     path('add_category/' , views.category, name='add_category'),
     path('add_dish/' , views.dish , name='add_dish'),
     path('add_carousel/' , views.carousel , name='add_carousel'),
     path('carousel_table/' , views.carousel_table , name='carousel_table'),
     path('carousel_delete/<int:id>' ,views.carousel_delete , name='carousel_delete'),
     path('carousel_edit/<int:id>' , views.carousel_edit , name='carousel_edit'),
     # path('profile/' , views.profile , name='profile'),
     path('category_table/' , views.category_table , name='category_table'),
     path('cat_edit/<int:id>' , views.category_edit ,name='cat_edit' ),
     path('cat_delete/<int:id>' , views.category_delete , name='cat_delete'),
     path('dish_table/' , views.dish_table , name='dish_table'),
     path('dis_delete/<int:id>' , views.dish_delete , name='dish_delete'),
     path('dish_edit/<int:id>', views.dish_edit , name='dish_edit'),
     path('contact_table/' , views.contact_table , name='contact_table' ),
     path('delete_table/<int:id>' , views.delete_contact , name='delete_contact'),
     path('order_table/' , views.order_table , name='order_table'),
     path('order_delete/<int:id>' , views.order_delete , name='order_delete'),
     path('user_table/' , views.user_table, name='user_table'),
     path('delete_user/<int:id>' , views.delete_user , name='delete_user'),
     path('update_user/<int:id>' , views.update_user , name='update_user'),
     path('add_user/' , views.add_user , name='add_user'),
     path('profile_table/' , views.profile_table ,name='profile_table'),
     path('profile_update/<int:id>' , views.update_profile , name='profile_update'),
     path('user_logout/' , views.user_logout , name='user_logout'),

]

if settings.DEBUG:
    urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)