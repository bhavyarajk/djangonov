from django.shortcuts import render,redirect
from shop.models import Category,Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView,DeleteView,UpdateView
class allcategories(ListView):
    model=Category
    template_name='category.html'
    context_object_name="c"

# def allcategories(request):
#     c=Category.objects.all()
#     return render(request,'category.html',{'c':c})

# def allproducts(request,p):
#     c=Category.objects.get(name=p)
#     p=Product.objects.filter(category=c)
#     return render(request,'product.html',{'c':c,'p':p})
class allproducts(DetailView):
    model=Category
    template_name='product.html'
    context_object_name="c"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj=super().get_object()
        p = Product.objects.filter(category=obj)
        context['p']=p
        return context




# def deatil(request,p):
#     product=Product.objects.get(name=p)
#
#     return render(request,'detail.html',{'p':product})
class detail(DetailView):
    model=Product
    template_name='detail.html'
    context_object_name="p"


def register(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        cp=request.POST['cp']
        e=request.POST['e']

        if(p==cp):
            u=User.objects.create_user(username=u,password=p,email=e)
            u.save()
            return redirect('shop:allcat')
        else:
            return HttpResponse("Password Not matching")


    return render(request,'register.html')
def user_login(request):
    if(request.method=="POST"):
        name=request.POST['u']
        pass1=request.POST['p']
        user=authenticate(username=name,password=pass1)
        if user:
            login(request,user)
            return redirect('shop:allcat')
        else:
            messages.error(request,"Invalid Credentails")
    return render(request,'login.html')


@login_required
def user_logout(request):
    logout(request)
    return user_login(request)

