from django.shortcuts import render,redirect
from shop.models import Category,Product
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
def allcategories(request):
    c=Category.objects.all()
    return render(request,'category.html',{'c':c})


def allproducts(request,p):
    c=Category.objects.get(name=p)
    p=Product.objects.filter(category=c)
    return render(request,'product.html',{'c':c,'p':p})
def detail(request,p):
    p=Product.objects.get(name=p)
    return render(request,'detail.html',{'p':p})
def register(request):
    if(request.method=="POST"):#After form submission
        u=request.POST['u']
        p=request.POST['p']
        cp=request.POST['cp']
        fname=request.POST['f']
        lname=request.POST['l']
        e=request.POST['e']
        if(p==cp):
            user=User.objects.create_user(username=u,password=p,first_name=fname,last_name=lname,email=e)
            user.save()
            return redirect('shop:allcat')
        else:
            return HttpResponse("Passwods are not same")
    return render(request,'register.html')

def user_login(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return redirect('shop:allcat')
        else:
            return HttpResponse("Invalid Credentials")
    return render(request,'login.html')
@login_required
def user_logout(request):
    logout(request)
    return redirect('shop:login')



