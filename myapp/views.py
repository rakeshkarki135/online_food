from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.http  import HttpResponse,JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from .forms import CheckoutForm



# Create your views here.
def index(request):
     carousel_item = CarouselItems.objects.all()
     category_items = Category.objects.all()
     data={
          'carousel' : carousel_item ,
          'category' : category_items
          }
     
     return render(request , 'myapp/index.html' , data )
    

def menu(request):
     category_items = Category.objects.all()
     
     # if "cate_id" in request.GET:
     #      selected_id = request.GET.get('cate_id')
     #      dish_items = Dish.objects.filter(category=selected_id)
     #      print(selected_id)
          
     data = {
          'category' : category_items,
     }
     return render(request , 'myapp/menu.html' , data)


def team(request):
     return render(request , 'myapp/team.html')

def about(request):
     return render(request , 'myapp/about.html')

def contact(request):
     if request.method == "POST":
          name=request.POST.get('name')
          email=request.POST.get('email')
          sub=request.POST.get('subject')
          msg=request.POST.get('message')
          
          obj=Contact(name=name,email=email,subject=sub,message=msg)
          obj.save()
          messages.info(request, f"Thank you {name} for your Concern" )
               
          
     return render(request , 'myapp/contact.html')

def feature(request):
     return render(request , 'myapp/feature.html')

def signin(request):
     context={}
     if request.method == "POST":
          username = request.POST.get('email')
          psw = request.POST.get('password')
          
          try:
               user_obj = User.objects.filter(username=username).first()
               
               if user_obj is None:
                    context.update({'message':' User doesnot exist' , 'class':'alert-danger'})
                    return render(request, 'myapp/signin.hmtl' , context)
               
               check_user = authenticate(username=username,password=psw)
               if check_user: 
                    login(request , check_user)
                    messages.info(request,'logged in Successfully')
                    # redirect to dashboard link here
                    if check_user.is_superuser or check_user.is_staff:
                         return redirect('/admin/')
                    # context.update({'message':'Login Success','class':'alert-success'})
                    return redirect('index')
                    
               else:
                    context.update({'message':'Invalid Login Details','class':'alert-danger' })
                    return render(request, 'myapp/signin.html', context)
          except Exception as e:
               pass
     
     return render(request ,  'myapp/signin.html',context)

def dashboard(request):
     context={}
     
     if request.user.is_authenticated:
          
          # getting the user
          login_user = request.user
          #fetch login user's data having username = request.user.username
          profile = Profile.objects.get(user=login_user)
          context['profile'] = profile
          
          try:
               cart = Cart.objects.get(user=login_user)
          except:
               cart = None
               
          if cart:
               # get the ordered items associated with cart
               ordered_items = CartItems.objects.filter(cart=cart)
               order = Order.objects.filter(cart=cart)
               context['ordered_items'] = ordered_items
               context['orders'] = order
               
       
          #update_profile
          if  "update_profile" in request.POST:
              name=request.POST.get('name')
              email=request.POST.get('email')
              contact=request.POST.get('number')
              add=request.POST.get('address')
          
              profile.user.first_name = name
              profile.user.save()
              profile.contact_number =contact
              profile.address = add
              profile.save()
              if "profile_pic"  in request.FILES:
                 pic = request.FILES.get('profile_pic')
                 profile.profile_pic = pic
                 profile.save()
                 context['status'] = 'Profile Updated Successfully'
            
          #changePassword
          if  "change_pass"  in request.POST:
              c_password = request.POST.get('current_password')
              n_password = request.POST.get('new_password')
            
              check = login_user.check_password(c_password)
              if check == True:
                  login_user.set_password(n_password)
                  login_user.save()
                  # logging in user
                  # login(request , login_user)     
                  context['status'] = 'Password Updated Successfully'
              else:
                  context['status'] = 'Current Password Incorrect'
                 
     return render(request , 'myapp/dashboard.html', context)
            
            
def register(request):
     context={}
     if request.method=="POST":
          # fetch data from html form
          name=request.POST.get('name')
          email=request.POST.get('email')
          password=request.POST.get('pass')
          contact=request.POST.get('number')
          
          
          try:
               if User.objects.filter(email=email).first():
                    messages.info(request, 'Email is already taken')
                    return redirect('register')
               elif User.objects.filter(username=name).first():
                    messages.info(request, 'Username is already taken')
                    return redirect('register')
               else:
                    # save data to both tables
                    user=User.objects.create_user(username=name,email=email,password=password)
                    user.save()
                    
                    # creating profiles
                    profile=Profile(user=user,contact_number=contact)
                    profile.save()
                    context['status'] = f"User {name} Registered Successfully!"
                    return render(request, 'myapp/signin.html', context)
               
          except Exception as e:
               pass
     return render(request , 'myapp/register.html', context)


def check_user_exist(request):
     email=request.GET.get('usern')
     check=User.objects.filter(username=email)
     if len(check) == 0:
          return JsonResponse({'status':0,'message':'Not Exist'})
     else:
          return JsonResponse({'status':1,'message':'A user with this email already Exist'})     
     
def logout_user(request):
     logout(request)
     messages.info(request,"Logged out successfully")
     return redirect('signin')

def dish(request ,id):
     context = {}
     dish = get_object_or_404(Dish, id=id)
     context.update({'dish':dish })   
     return render(request , 'myapp/dish.html', context )


def alldishes(request):
    context = {}
    dishes = Dish.objects.all()

    if "q" in request.GET:
        id = request.GET.get('q')
        category = Category.objects.get(id=id)
        dishes = Dish.objects.filter(category=category)
        context['dish_category'] = category.name

    context['dishes'] = dishes
    return render(request, 'myapp/all_dishes.html', context)

def payment_done(request):
     pid = request.GET.get('player_id')
     order_id = request.session.get('order_id')
     order_obj = Order.objects.get(id=order_id)
     order_obj.status = True
     order_obj.player_id = pid
     order_obj.save()
     return render(request, 'myapp/payment_successfull.html')


def payment_failed(request):
     order_id = request.session.get('order_id')
     Order.objects.get(id=order_id).delete()
     return render(request , 'myapp/payment_failed.html')


def add_to_cart(request , id):
     dish =  Dish.objects.get(id=id)
     user = request.user
     
     # getting or creating cart for user
     cart , _ = Cart.objects.get_or_create(user=user , is_paid = False)
     
     # checking if same dish  alerady exist in cart 
     existing_cart_item, created = CartItems.objects.get_or_create(cart=cart , dish=dish)
     
     try:
          
        if not created:
            # update the quantity
            existing_cart_item.quantity += 1
            existing_cart_item.save()
     except:
          pass
     
     return redirect('alldishes')

def remove_cart(request , cart_item_id):
     try:
        cart_item = CartItems.objects.get(id=cart_item_id)
        cart_item.delete()
        
     except:
          pass
     
     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
     

def cart(request):
     cart = Cart.objects.filter(user=request.user , is_paid=False).first()
     if cart:
         cart_item = CartItems.objects.filter(cart=cart)
     else:
         cart_item = []
          
     return render(request, 'myapp/cart.html' , { 'items':cart_item })


@require_POST
@csrf_protect
def update_cart_item(request):
     item_id = request.POST.get('item_id')
     quantity = int(request.POST.get('quantity'))
     
     try:
          cart_item = CartItems.objects.get(id=item_id)
          cart_item.quantity = quantity
          cart_item.save()
          
          # calculate the new total price for item
          total_price = 0
          total_price = cart_item.dish.discount_price * quantity
          
          # calculate the new cart total price 
          cart = cart_item.cart
          
          cart_total = sum(item.get_product_price() for item in cart.cart_items.all())
          
          return JsonResponse({'total_price':total_price , 'cart_total':cart_total })
     
     except CartItems.DoesNotExist:
          return JsonResponse({'error':'Cart item not found'})
          

def khlatirequest(request):
     return render(request , 'myapp/khaltipaymentrequest.html')
     


def checkout(request):
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                # Assuming you have a 'cart' object, you should retrieve it based on your application's logic
                user = request.user # Modify this to get the user's cart
                user_cart = Cart.objects.get(user=user , is_paid=False)
                total_price = user_cart.calculate_total_price()  # Calculate the total price

                # Create an Order instance with the form data and the total price
                order = Order(
                    user = user,
                    ordered_by=form.cleaned_data['ordered_by'],
                    shipping_address=form.cleaned_data['shipping_address'],
                    cart = user_cart,
                    mobile=form.cleaned_data['mobile'],
                    email=form.cleaned_data['email'],
                    total=total_price,
                    order_status="Order Completed",
                    payment_method=form.cleaned_data['payment_method'],
                    payment_completed=False,
                   
                )
                order.save()
                # Save the order to the database

                messages.success(request, "Order placed successfully")
                user_cart=0
                total_price=0
                return redirect('alldishes')  # Redirect to the thank you page

            except Exception as e:
                pass
        else:
            messages.error(request, "Form is not valid. Please check your input.")
    else:
        form = CheckoutForm()

    return render(request, 'myapp/checkout.html', {'form': form})



