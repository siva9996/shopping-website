from django.shortcuts import render,redirect
from .forms import Usercreation
from .models import *
from django.contrib.auth import logout
from datetime import datetime,date,timedelta
from django.contrib import messages
from django.db.models import Q
# Create your views here.

def home(request):
    prod=product.objects.filter(trending=1)
    if request.method=='POST':
        if request.POST.get('q').isalpha() or request.POST.get('q').isdigit():
            q = request.POST.get('q')
        else:
            q="tq"
        if q == "tp":
            context={'prod':prod}
        else:
            searchprod=product.objects.filter(Q(name__icontains=q) | Q(category__name__icontains=q) )
            searchprod_count=searchprod.count()
            print(searchprod_count)
            if searchprod_count > 0:
                context={'searchprod':searchprod}
            else:
                messages.warning(request,"No product found")
                context={'prod':prod}
    else:
        context={'prod':prod}
    return render(request,'base/home.html',context)

def category(request):
    cate=Category.objects.all()
    return render(request,'base/category.html',{'cate':cate})

def products(request,id):
    prod=product.objects.filter(category_id=id)
    return render(request,'base/products.html',{'prod':prod})

def productdes(request,id):
    prod=product.objects.get(id=id)
    return render(request,'base/productdes.html',{'prod':prod})

def buy(request,id):
    if request.session.get('username'):
        name1=request.session['username']
        user1=user.objects.get(username=name1)
        buy=Buyproduct.objects.filter(user=user1)
        cart=Cart.objects.filter(user=user1)
        print(cart)
        today=date.today()
        time=today+timedelta(days=7)
        if request.method=='POST':
            val=request.POST.get('buyval')
            val=int(val)
            prod1=product.objects.get(id=id)
            a=Buyproduct.objects.filter(name=prod1.name)
            b=1
            for i in (a):
                if i.user.username==user1.username and i.confirm==0:
                    b=2
                    break
                else:
                    b=1
            if (a.exists()) and b==2:
                messages.warning(request,'This product already in your cart')
                return redirect('productdes',prod1.id)
            else:
                name1=request.session['username']
                user1=user.objects.get(username=name1)
                overallpr=val*prod1.selling_price
                if val > prod1.quantity:
                    messages.warning(request,'Your order count is not available in stock')
                    return redirect('productdes',prod1.id)
                else:
                    for i in cart:
                        if i.prod.name==prod1.name:
                            i.delete()
                    Buyproduct.objects.create(prod=prod1,user=user1,name=prod1.name,product_image=prod1.product_image,quantity=val,selling_price=prod1.selling_price,overallprice=overallpr,description=prod1.description).save()
    else:
        return redirect('login')
    return render(request,'base/buy.html',{'buy':buy})

def buyu(request,id):
    name1=request.session['username']
    user1=user.objects.get(username=name1)
    buy=Buyproduct.objects.filter(user=user1)
    buy1=Buyproduct.objects.get(id=id)
    # prod=product.objects.get(id=id)
    today=buy1.updated
    time=today+timedelta(days=7)
    time=time.strftime('%b-%d')
    if request.method=='POST':     
        val=request.POST.get('but')
        if val=='confirm':
            if (Buyproduct.objects.filter(name=buy1.name).exists()) and buy1.confirm==1:
                pass
            else:
                if buy1.prod.quantity >= buy1.quantity:
                    buy1.confirm=True
                    buy1.delivery=time
                    buy1.prod.quantity=buy1.prod.quantity-buy1.quantity
                    buy1.save()
                    buy1.prod.save()
                    messages.error(request,'Your order successfully placed')
                else:
                    print("Your order count is not available in stock")
    return render(request,'base/buy.html',{'buy':buy})

def orders(request):
    name1=request.session['username']
    user1=user.objects.get(username=name1)
    buy=Buyproduct.objects.filter(user=user1)
    # today=buy.updated
    # time=today+timedelta(days=7)
    return render(request,'base/buy.html',{'buy':buy})

def cancelorder(request,id):
    Buyprod=(Buyproduct.objects.get(id=id))
    Buyprod.prod.quantity=Buyprod.quantity+Buyprod.prod.quantity
    Buyprod.prod.save()
    Buyprod.delete()
    messages.error(request,'Your Cancel request accepted')
    return redirect('orders')

def nccancelorder(request,id):
    Buyprod=(Buyproduct.objects.get(id=id))
    Buyprod.prod.save()
    Buyprod.delete()
    messages.error(request,'Cart item removed')
    return redirect('orders')
    
def cart(request,id):
    if request.session.get('username'):
        name1=request.session['username']
        user1=user.objects.get(username=name1)
        carts=Cart.objects.filter(user=user1)
        if request.method=='POST':
            val=request.POST.get('cartval')
            val=int(val)
            prod1=product.objects.get(id=id)

            a=Cart.objects.filter(name=prod1.name)
            b=1
            for i in (a):
                if i.user.username==user1.username:
                    b=2
                    break
                else:
                    b=1
            if (a.exists()) and b==2:
                messages.warning(request,'This product already in your cart')
                return redirect('productdes',prod1.id)

            # if (Cart.objects.filter(name=prod1.name).exists()):
            #     messages.warning(request,'This product already in your cart')
            #     return redirect('productdes',prod1.id)
                # return redirect('carts')
            name1=request.session['username']
            user1=user.objects.get(username=name1)
            overallpr=val*prod1.selling_price
            Cart.objects.create(prod=prod1,user=user1,name=prod1.name,product_image=prod1.product_image,quantity=val,selling_price=prod1.selling_price,overallprice=overallpr,description=prod1.description).save()
    else:
        return redirect('login')
    return render(request,'base/cart.html',{'carts':carts})

def carts(request):
    name1=request.session['username']
    user1=user.objects.get(username=name1)
    cart=Cart.objects.filter(user=user1)
    return render(request,'base/carts.html',{'cart':cart})

def removecart(request,id):
    cart=(Cart.objects.get(id=id))
    cart.delete()
    return redirect('carts')

def Login_page(request):
    if request.method=='POST':
        name=request.POST.get('username')
        pass1=request.POST.get('password')
        user1=user.objects.get(username=name)
        if user1.username==name and user1.password==pass1:
            request.session['username']=user1.username
            request.session['email']=user1.email
            return redirect('home')
        else:
            print('user does not exist')
    return render(request,'base/login.html')

def Logout(request):
    logout(request)
    return redirect('home')

def register_page(request):
    form=Usercreation()
    if request.method=='POST':
        form=Usercreation(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request,'base/register.html',{'form':form})