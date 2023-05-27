from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, CustomAuthenticationForm, SortingForm, BrandForm
from .models import Perfume, Brand, Cart


# Create your views here.
def index(request):
    perfumes = Perfume.objects.all()[:4]
    context = {'perfumes': perfumes}
    return render(request, 'index.html', context)


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def shop(request):
    brands = Brand.objects.all()
    brand_form = BrandForm(request.GET)
    sorting = SortingForm(request.GET)
    query = request.GET.get('query')
    sorting_option = request.GET.get('sorting_option')

    perfumes = Perfume.objects.all()

    if sorting_option == 'price_low_high':
        perfumes = perfumes.order_by('price')
    elif sorting_option == 'price_high_low':
        perfumes = perfumes.order_by('-price')

    if brand_form.is_valid():
        selected_brands = brand_form.cleaned_data['brand_choices']
        if selected_brands:
            perfumes = perfumes.filter(brand__in=selected_brands)

    if query:
        perfumes = perfumes.filter(name__icontains=query)

    if 'clear' in request.GET:
        # Clear all form data
        return HttpResponseRedirect(request.path)

    context = {
        'perfumes': perfumes,
        'sorting': sorting,
        'brands': brands,
        'query': query,
        'brand_form': brand_form,
    }
    return render(request, 'shop.html', context)


def info(request):
    return render(request, 'info.html')


@login_required
def cart(request):
    # Retrieve the cart items for the current user
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.perfume.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)


@login_required
def add_to_cart(request, perfume_id):
    perfume = Perfume.objects.get(id=perfume_id)
    cart_item = Cart.objects.filter(user=request.user, perfume=perfume).first()

    if cart_item:
        # If the cart item already exists, increase the quantity
        cart_item.quantity += 1
        cart_item.save()
    else:
        # If the cart item doesn't exist, create a new one with quantity 1
        cart_item = Cart(user=request.user, perfume=perfume)
        cart_item.save()

    return redirect('cart')


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = Cart.objects.get(id=cart_item_id)
    cart_item.delete()

    return redirect('cart')


@login_required
def remove_one_from_cart(request, cart_item_id):
    cart_item = Cart.objects.get(id=cart_item_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


def clear_cart(request):
    Cart.objects.all().delete()
    return redirect('index')


def perfume_detail(request, slug):
    perfume = get_object_or_404(Perfume, url_name=slug)
    context = {
        'perfume': perfume
    }
    return render(request, 'perfume_detail.html', context)
