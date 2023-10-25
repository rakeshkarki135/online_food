from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path('',views.index, name='index'),
     path('signin/',views.signin,name='signin'),
     path('register/',views.register,name='register'),
     path('menu/',views.alldishes,name='menu'),
     path('team/',views.team,name='team'),
     path('about',views.about,name='about'),
     path('contact/',views.contact,name='contact'),
     path('feature/',views.feature,name='feature'),
     path('check_user_exist/',views.check_user_exist,name='check_user_exist'),
     path('dashboard/',views.dashboard,name='dashboard'),
     path('logout_user/',views.logout_user,name='logout_user'),
     path('dish/<int:id>',views.dish,name='dish'),
     path('alldishes/',views.alldishes,name='alldishes'),
     path('khalti_request/' , views.khlatirequest , name='khalti_request'),
     path('paypal/',include('paypal.standard.ipn.urls')),
     path('payment_done/',views.payment_done,name='payment_done'),
     path('payment_failed/',views.payment_failed,name='payment_failed'),
     path('add_to_cart/<int:id>' , views.add_to_cart, name='add_to_cart'),
     path('remove_cart/<cart_item_id>' , views.remove_cart ,name='remove_cart'),
     path('cart/' ,views.cart, name='cart'),
     path('checkout/' , views.checkout , name='checkout'),
     path('update_cart_item/' , views.update_cart_item , name='update_cart_item'),

]

if settings.DEBUG:
    urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)