from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from ecom import forms
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.conf import settings
from ecom import models
from ecom.cart import Cart
from .forms import CartAddProductForm, OrderCreateForm


def home_view(request):
    products = models.Medicine.objects.all()

    return render(request, 'ecom/index.html', {'products': products})


def product_detail(request, id):
    product = get_object_or_404(models.Medicine, id=id)
    cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        'cart_product_form': cart_product_form,
    }
    return render(request, 'ecom/product_detail.html', context)


def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()


def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('customer-home')
    else:
        return redirect('/admin')


def customer_signup_view(request):
    userForm = forms.CustomerUserForm()
    customerForm = forms.CustomerForm()
    mydict = {'userForm': userForm, 'customerForm': customerForm}
    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST)
        customerForm = forms.CustomerForm(request.POST, request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customer = customerForm.save(commit=False)
            customer.user = user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    return render(request, 'ecom/customersignup.html', context=mydict)


def aboutus_view(request):
    return render(request, 'ecom/aboutus.html')


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def my_profile_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    return render(request, 'ecom/my_profile.html', {'customer': customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def edit_profile_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    user = models.User.objects.get(id=customer.user_id)
    userForm = forms.CustomerUpdateUserForm(instance=user)
    customerForm = forms.CustomerForm(instance=customer)
    mydict = {'userForm': userForm, 'customerForm': customerForm}
    if request.method == 'POST':
        userForm = forms.CustomerUpdateUserForm(request.POST, instance=user)
        customerForm = forms.CustomerForm(request.POST, request.FILES, instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.save()
            customerForm.save()
            return HttpResponseRedirect('my-profile')
    return render(request, 'ecom/edit_profile.html', context=mydict)


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_home_view(request):
    products = models.Medicine.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0
    return render(request, 'ecom/customer_home.html',
                  {'products': products, 'product_count_in_cart': product_count_in_cart})


# any one can add product to cart, no need of signin
def add_to_cart_view(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(models.Medicine, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'ecom/cart_detail.html', {'cart': cart})


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(models.Medicine, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        print('cd = ', cd)
        cart.update(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(models.Medicine, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = models.User.objects.get(username=request.user)
            order = models.Orders.objects.create(
                user=user,
                email=cd['email'],
                mobile=cd['mobile'],
                address=cd['address'],
                total_price=cart.get_total_price()
            )

            for item in cart:
                models.OrderItem.objects.create(
                    order=order,
                    medicine=item['product'],
                    price=item['selling_price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return render(request, 'ecom/order_created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'ecom/checkout_create.html', {'form': form})


def order_view(request):
    orders = models.Orders.objects.filter(user=request.user)
    return render(request, 'ecom/order_view.html', {'orders': orders})


def search_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    products = models.Medicine.objects.all().filter(name__icontains=query)

    # word variable will be shown in html when user click on search button
    word = "Searched Result : {}".format(query)

    return render(request, 'ecom/index.html', {'products': products, 'word': word, })


def order_details(request, order_id):
    orders = models.Orders.objects.get(user=request.user, id=order_id)
    products = models.OrderItem.objects.filter(order__id=order_id)
    return render(request, 'ecom/order_details.html', {'order': orders, "products": products})
