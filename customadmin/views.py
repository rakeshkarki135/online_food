from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from myapp.models import *


# Create your views here.
def admin_login(request):
     try:
          if request.user.is_authenticated:
               return redirect('admin_dashboard')
          # messages.info(request , 'Acount not found')
          if request.method == 'POST':
               username = request.POST.get('username')
               password = request.POST.get('password')
               user_obj = User.objects.filter(username = username)
               if not user_obj.exists():
                    messages.info(request , ' Account not Found ' )
                    return redirect('/admin/')
          
               user_obj = authenticate(username = username , password = password)
          
               if user_obj:
                    if user_obj.is_superuser or user_obj.is_staff:
                       login(request , user_obj)
                       return redirect('admin_dashboard') 
                    
                    messages.info(request , ' Account not Found ')
                    return redirect('/admin/')
          
               messages.info(request , ' Invalid Login Details ')
               return redirect('/admin/')
          
          return render(request , 'customadmin/login.html' )
     
     except Exception as e:
          print(e)
          
def admin_dashboard(request):
     return render(request , 'customadmin/index.html')

def table(request):
     return render(request , 'customadmin/table.html')

def category(request):
     context = {}
     obj = Category.objects.all()
     
     if 'add_category' in request.POST:
          name = request.POST.get('name')
          image = request.FILES.get('image')
          icon = request.POST.get('icon')
          description = request.POST.get('description')
          
          try:
            cat_items=Category(name=name,image=image,icon=icon,description=description)
            cat_items.save()
            messages.success(request,'Category added Successfully')
            return redirect('category')
            
          except :
            pass
          messages.error(request , f'Failed to add the {name}')
     context['obj']=obj     
     return render ( request , 'customadmin/category.html' , context)


def dish(request):
    obj = Category.objects.all()  # Rename 'obj' to 'categories' for clarity

    if request.method == 'POST':
        name = request.POST.get('name')
        ingredients = request.POST.get('ingredients')
        details = request.POST.get('details')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        discount_price = request.POST.get('discount_price')
        is_available = request.POST.get('available') == 'on'

        try:
            # Get the category object with the specified ID
            category = Category.objects.get(id=category_id)
            dish_obj = Dish(
                name = name,
                ingredients = ingredients,
                details = details,
                category = category,
                price = price,
                discount_price = discount_price,
                is_available = is_available
            )
            dish_obj.save()
            
            if 'dish_img' in request.FILES:
                 pic = request.FILES.get('dish_img')
                 dish_obj.image = pic
                 dish_obj.save()
                 
            messages.success(request, 'Dish added successfully')
            return redirect('dish')  # Redirect to the 'dish' URL
        except Category.DoesNotExist:
            messages.error(request, 'Invalid category ID')  # Handle the case where the category does not exist
        except :
            pass

    return render(request, 'customadmin/dish.html', { 'objs': obj })


def carousel(request):
     if request.method == "POST":
          first_title = request.POST.get('first_title')
          span_title = request.POST.get('span_title')
          last_title = request.POST.get('last_title')
          text = request.POST.get('text')
          
          try:
               carousel_item = CarouselItems(first_title=first_title,span_title=span_title,last_title=last_title,text=text)
               carousel_item.save()
               
               if 'car_img' in request.FILES:
                    pic = request.FILES.get('car_img')
                    carousel_item.image = pic
                    carousel_item.save()
               
               messages.success(request , 'Carousel item added Successfully')
               redirect('carousel')
               
          except Exception as e:
               messages.error(request , 'Failed to insert Carousel Item')
                    
     return render(request , 'customadmin/carousel.html')

def carousel_table(request):
     carousel = CarouselItems.objects.all()
     return render(request , 'customadmin/carousel_table.html' , {'carousel':carousel})

def carousel_delete(request , id):
     carousel = get_object_or_404(CarouselItems , id=id )
     carousel.delete()
     return redirect('carousel_table')

def carousel_edit(request , id):
     carousel = get_object_or_404(CarouselItems , id=id)
     
     if 'add_carousel' in request.POST:
          image = request.FILES.get('car_img') 
          first_title = request.POST.get('first_title')
          span_title = request.POST.get('span_title')
          last_title = request.POST.get('last_title')
          text = request.POST.get('text')
          
          try:
               carousel.image = image
               carousel.first_title = first_title
               carousel.span_title = span_title
               carousel.last_title = last_title
               carousel.text = text
               carousel.save()
               messages.success(request , 'Carousel Updated Successfully')
               return redirect('carousel_table')
               
          except Exception:
               messages.error(request , 'An error Occured')
          
     return render(request , 'customadmin/carousel.html' ,{ 'carousel':carousel})
          
          
def contact_table(request):
     contact = Contact.objects.all()
     return render(request  , 'customadmin/contact_table.html' ,{ 'contact':contact })
          
def delete_contact(request , id):
     contact = get_object_or_404(Contact , id=id)
     contact.delete()
     return redirect('contact_table')
     

# def profile(request):
#      if request.method == "POST":
#           usr = request.POST.get('usr') 
#           profile_pic = request.FILES.get('profile_pic')
#           contact_number = request.POST.get('contact')
#           address = request.POST.get('address')
          
#           try:
#                user_obj = User()


def category_table(request):
     context={}
     obj = Category.objects.all()     
     return render(request , 'customadmin/category_table.html' , { 'obj':obj })

def category_edit(request , id):
     category = Category.objects.get(id=id)
       
     if 'add_category' in request.POST:
          name = request.POST.get('name')
          image = request.FILES.get('image')
          icon = request.POST.get('icon')
          description = request.POST.get('description')
          
          try:
            category.name = name
            category.image = image
            category.icon = icon
            category.description = description
            category.save()
            messages.success(request , 'Category Updated Successfully')
            return redirect('category_table')
       
          except:
               pass
     
     return render(request , 'customadmin/category.html' ,{'category':category} )

def category_delete(request , id):
     category = Category.objects.get(id=id)
     category.delete()
     return redirect('category_table')

def dish_table(request):
     dish = Dish.objects.all()
     return render(request , 'customadmin/dish_table.html', {'objs': dish}) 

def dish_delete(request , id ):
     dish = Dish.objects.filter(id=id)
     dish.delete()
     return redirect('dish_table')


def dish_edit(request, id):
    dish = get_object_or_404(Dish, id=id)
    categories = Category.objects.all()
    
    if request.method == "POST":
        name = request.POST.get('name')
        image = request.FILES.get('dish_img')
        ingredients = request.POST.get('ingredients')
        details = request.POST.get('details')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        discount_price = request.POST.get('discount_price')
        is_available = request.POST.get('available') == 'on'
        
        try:
            category = get_object_or_404(Category, id=category_id)
            dish.name = name
            dish.image = image
            dish.ingredients = ingredients
            dish.details = details
            dish.category = category
            dish.price = price
            dish.discount_price = discount_price
            dish.is_available = is_available
            dish.save()
            messages.success(request, 'Dish Updated Successfully')
            return redirect('dish_table')
            
            
        except Category.DoesNotExist:
            messages.error(request, 'Selected category does not exist.')
            
    return render(request , 'customadmin/dish.html' , { 'obj':dish , 'objs':categories })

def order_table(request):
     order = Order.objects.all()
     return render(request , 'customadmin/order_table.html' , { 'order':order})

def order_delete(request , id):
     order = get_object_or_404(Order , id=id)
     order.delete()
     return redirect('order_table')

def user_table(request):
     usr = User.objects.all()
     return render(request , 'customadmin/user_table.html' , { 'usr':usr })

def delete_user(request , id):
     usr = get_object_or_404( User , id=id)
     usr.delete()
     return redirect('user_table')
     
def update_user(request , id):
     usr = get_object_or_404(User , id=id)
     if request.method == 'POST':
          username = request.POST.get('username')
          password = request.POST.get('password')
          first_name = request.POST.get('first_name')
          last_name = request.POST.get('last_name')
          email = request.POST.get('email')
          is_active = request.POST.get('is_active') == 'on'
          is_staff = request.POST.get('is_staff')  == 'on'
          is_superuser = request.POST.get('is_superuser') == 'on'
          print(is_superuser)
          
          try:
               usr.username = username
               usr.set_password(password)
               usr.first_name = first_name
               usr.last_name = last_name
               usr.email = email
               usr.is_active = is_active
               usr.is_staff = is_staff
               usr.is_superuser = is_superuser
               usr.save()
               messages.success(request , ' User updated Successfully')
               return redirect('user_table')
          
          except:
               pass
     return render(request , 'customadmin/update_user.html' , {'usr':usr})

def add_user(request):
     if request.method == 'POST':
          username = request.POST.get('username')
          first_name = request.POST.get('first_name')
          last_name = request.POST.get('last_name')
          password = request.POST.get('password')
          conform_password = request.POST.get('password1')
          
          
          if password == conform_password:
               user = User.objects.create_user(username=username , password=password ,first_name=first_name , last_name=last_name)
               user.save()
               
               # creating profile
               profile = Profile(user=user)
               profile.save()
               messages.success(request , 'User created Successfully')
               return redirect('user_table')
          
          else:
               redirect('add_user')
               messages.error(request , 'Check the passwords')
              
               
          
     return render(request , 'customadmin/add_user.html')


def profile_table(request):
     profile = Profile.objects.all()
     return render(request , 'customadmin/profile_table.html' , { 'usr' : profile })

def update_profile(request ,id):
     profile = get_object_or_404(Profile , id=id)
     
     if request.method == 'POST':
          name = request.POST.get('name')
          profile_pic = request.FILES.get('profile_pic')
          contact_number = request.POST.get('contact_number')
          address = request.POST.get('address')
          
          try:
               profile.user.first_name = name
               profile.profile_pic = profile_pic
               profile.contact_number = contact_number
               profile.address = address
               profile.save()
               messages.success(request , f'{name} profile Updated Succcessfully' )
               return redirect('profile_table') 
              
          
          except:
               pass
          
     return render(request , 'customadmin/update_profile.html' , { 'profile':profile })


def user_logout(request):
     logout(request)
     messages.success(request , 'Logged out Successfully')
     return redirect('admin_login')