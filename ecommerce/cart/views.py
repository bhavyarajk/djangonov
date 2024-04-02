from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from shop.models import Product
from cart.models import Cart
from cart.models import Account,Order
from django.views.generic import ListView,DetailView

# def cartview(request):
#     total=0
#     u=request.user
#     try:
#         cart=Cart.objects.filter(user=u)
#         for i in cart:
#             total+=i.quantity*i.product.price
#
#
#
#     except:
#         pass
#
#
#     return render(request,'cart.html',{'c':cart,'total':total})
class cartview(ListView):
    login_required = True
    model=Cart
    template_name="cart.html"


    def get_context_data(self, *, object_list=None, **kwargs):
        u=self.request.user
        cart=self.get_queryset().filter(user=u)
        total=0
        for i in cart:
              total+=i.quantity*i.product.price
        context=super().get_context_data()
        context['c']=cart
        context['total']=total
        return context

class add_to_cart(DetailView):
      model=Product

      def get(self,request,pk):
          u = self.request.user
          product = self.get_object()
          try:
              cart = Cart.objects.get(user=u, product=product)
              if (cart.quantity < cart.product.stock):
                  cart.quantity += 1
                  cart.product.stock -= 1

                  cart.product.save()
                  print(cart.product.stock)
              cart.save()
          except:

              cart = Cart.objects.create(product=product, user=u, quantity=1)
              cart.save()
              cart.product.stock -= 1

              cart.product.save()
              print(cart.product.stock)

          return redirect('cart:cartview')




#
#
# def add_to_cart(request,p):
#     product=Product.objects.get(name=p)
#     u=request.user
#     try:
#         cart=Cart.objects.get(user=u,product=product)
#         if(cart.quantity < cart.product.stock):
#             cart.quantity += 1
#             cart.product.stock -= 1
#
#             cart.product.save()
#             print(cart.product.stock)
#         cart.save()
#     except:
#         cart=Cart.objects.create(product=product,user=u,quantity=1)
#         cart.save()
#         cart.product.stock -= 1
#
#         cart.product.save()
#         print(cart.product.stock)
#
#
#     return redirect('cart:cartview')

class cart_remove(DetailView):
    model=Product

    def get(self, request, pk):
        u = self.request.user
        product = self.get_object()
        try:
            cart = Cart.objects.get(user=u, product=product)
            if cart.quantity>1:
                cart.quantity-=1
                cart.product.stock += 1
                cart.product.save()
                print(cart.product.stock)

                cart.save()
            else:
                cart.product.stock += 1
                cart.product.save()
                cart.delete()
        except:
            pass
        return redirect('cart:cartview')


# def cart_remove(request,p):
#     p=Product.objects.get(name=p)
#     user=request.user
#     try:
#         cart=Cart.objects.get(user=user,product=p)
#         if cart.quantity>1:
#             cart.quantity-=1
#             cart.product.stock += 1
#             cart.product.save()
#             print(cart.product.stock)
#
#             cart.save()
#         else:
#             cart.product.stock += 1
#             cart.product.save()
#             cart.delete()
#     except:
#         pass
#     return redirect('cart:cartview')
#

# def full_remove(request,p):
#     p=Product.objects.get(name=p)
#     user=request.user
#     try:
#         cart=Cart.objects.get(user=user,product=p)
#         print(cart.product.stock)
#         cart.product.stock += cart.quantity
#         cart.product.save()
#         print(cart.product.stock)
#
#         cart.delete()
#     except:
#         pass
#     return redirect('cart:cartview')

class full_remove(DetailView):
    model=Product
    def get(self,request,pk):
        p =self.get_object()
        user = self.request.user
        try:
            cart = Cart.objects.get(user=user, product=p)
            print(cart.product.stock)
            cart.product.stock += cart.quantity
            cart.product.save()
            print(cart.product.stock)

            cart.delete()
        except:
            pass
        return redirect('cart:cartview')


def orderform(request):
    if(request.method=="POST"):
        a=request.POST['a']
        p=request.POST['p']
        n=request.POST['n']
        u=request.user
        cart=Cart.objects.filter(user=u)

        #Total Amount
        total=0
        for i in cart:
            total+=i.quantity*i.product.price

        #check whether user has sufficient amount in his/her account.
        ac=Account.objects.get(acctnum=n)
        if(ac.amount>=total):
            ac.amount=ac.amount-total
            ac.save()

            for i in cart: #creates record in Order table for each object in Cart table for the current user
                o=Order.objects.create(user=u,product=i.product,address=a,phone=p,no_of_items=i.quantity,order_status="paid")
                o.save()


            cart.delete() #clears the cart items for the current user
            msg="Order Placed Successfully"
            return render(request,'orderdetail.html',{'m':msg})

        else:

            msg="Insufficient Amount in User Account.You cannot place order."


            return render(request, 'orderdetail.html', {'m': msg})
    return render(request,'orderform.html')


def orderview(request):
    u=request.user
    o=Order.objects.filter(user=u)
    return render(request,'orderview.html',{'u':u.username,'o':o})