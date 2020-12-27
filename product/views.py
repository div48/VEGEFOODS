from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.checks import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic.base import View
from .forms import *
from .models import *
from django import template


# def products(request):
#     product = Products.objects.all()
#     return render(request, "index1.html",  {product:'products'})
def index(request):
    dests = Products.objects.all()
    context = {
        'products': dests,

    }

    return render(request, "index1.html",context)

def cart(request):

    return render(request, "cart.html", )

def about(request):

    return render(request, "about.html", )

def home(request):
    return redirect("index")


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Products, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.Info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            order.items.add(order_item)
            messages.Info(request, "This item was added to your cart.")
            return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        print("1111111111111111111")
        messages.Info(request, "This item was added to your cart.")
        return redirect("order-summary")





@login_required()
def order_details(request, **kwargs):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        order1 = OrderItem.objects.filter(user=request.user,ordered=False).count()
        print(order1)
        context = {
        'order': order
             }
        return render(request, 'cart.html', context)
    except ObjectDoesNotExist:
        messages.WARNING(request, "You do not have an active order")
        return redirect("home")









@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Products, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.Info(request, "This item was removed from your cart.")
            return redirect("order-summary")
        else:
            messages.Info(request, "This item was not in your cart")
            return redirect()
    else:
        messages.Info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Products, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.Info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            messages.Info(request, "This item was not in your cart")
            return redirect("product", slug=slug)
    else:
        messages.Info(request, "You do not have an active order")
        return redirect("product", slug=slug)



@login_required
def checkout(request):

    order = Order.objects.get(user=request.user, ordered=False)
    order1 = OrderItem.objects.filter(user=request.user, ordered=False).count()
    print(order1)
    x=Address.objects.filter(user=request.user)
    print(x)
    print(request.user)
    if not x:
        print("not")
        return render(request, "address.html", )

    else:
        print("yes")
        context = {
                'order': order,
                'address':x
                }
        return render(request, "checkout.html",context )




@login_required
def add(request):
    print("add")
    if request.method == 'POST':
        print("step1")
        if request.POST.get('FirtName') and request.POST.get('LastName')and request.POST.get('address') and request.POST.get( 'town') and request.POST.get('pin') and request.POST.get('phone') and request.POST.get( 'email') :
            print("step2")

            FirtName =request.POST['FirtName']
            LastName =request.POST['LastName']
            address =request.POST['address']
            town =request.POST['town']
            pin =request.POST['pin']
            phone =request.POST['phone']
            email =request.POST['email']
            d = Address.objects.create(user=request.user,FirtName=FirtName,LastName=LastName,address=address,town=town,pincode=pin,phone=phone,email=email)
            print("3")
            d.save()
            print("4")
    return HttpResponseRedirect(reverse('checkout'))



def sucess(request):
    x= request.user
    order = Order.objects.filter(user=request.user, ordered=False)
    order.update(ordered=True)

    context = {
        'user':x
    }

    return render(request, "Sucess.html", context)
