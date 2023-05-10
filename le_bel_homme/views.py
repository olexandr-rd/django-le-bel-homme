from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, CustomAuthenticationForm, BrandForm
from .models import Perfume, Brand

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
                request.session['username'] = username
                response = redirect('index')
                response.set_cookie('username', username)
                return response
            else:
                form.add_error(None, 'Невірні дані користувача')
        else:
            print(form.errors)
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
    form = BrandForm()
    perfumes = Perfume.objects.all()
    context = {
        'perfumes': perfumes,
        'form': form,
        'brands': brands
    }
    return render(request, 'shop.html', context)


def info(request):
    return render(request, 'info.html')


def cart(request):
    chanel = Perfume.objects.get(name='Bleu de Chanel')
    guerlain = Perfume.objects.get(name='Guerlain L’Homme Idéal')
    perfumes = chanel, guerlain
    context = {
        'perfumes': perfumes
    }
    return render(request, 'cart.html', context)


def logout(request):
    request.session.clear()
    response = redirect('index')
    response.delete_cookie('username')
    return response

def perfume_detail(request, slug):
    perfume = get_object_or_404(Perfume, url_name=slug)
    context = {
        'perfume': perfume
    }
    return render(request, 'perfume_detail.html', context)