import datetime

from django.shortcuts import render,redirect
from django.contrib.auth .decorators import login_required
from django.contrib.auth import authenticate ,login ,logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from.forms import CustomUserCreationForm
from .models import CustomUser,Address,Subscription,Order

def home(request):
    return render(request)

def user_login(request):
    if request.method=='POST' :
        print(request.POST)
        username= request.POST.get('username','')
        password= request.POST.get('password','')
        user = authenticate(username=username , password=password)
        print(user)
        if user:
            login(request , user)
            return redirect("/")
    return render(request )

def user_logout(request): 
    logout(request)
    return redirect("/")

def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, {'form': form})

@login_required
def subscription(request):
    if request.method == 'POST':
        print(request.POST)
        # UserAdress=request.POST.get('adress')
        # Ordertime=request.POST.get('Order')
        # subscription_type=request.POST.get('subscription_type')

        # # if UserAdress exist in database then get it else create it
        # if Address.objects.filter(address_line=UserAdress).exists():
        #     UserAdress = Address.objects.get(address_line=UserAdress)
        # else:
        #     UserAdress = Address.objects.create(user=request.user, adress_line=UserAdress)
        
        # Order.objects.create(user=request.user, subscription=subscription, address=UserAdress, payment_date=Ordertime)
        # Subscription.objects.create(user=request.user,type = subscription_type ,expiration_date=datetime.now()+datetime.timedelta(days=30))

    return redirect('home')
