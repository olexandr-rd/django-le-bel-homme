from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, CustomAuthenticationForm
from .models import Perfume

# Create your views here.
def index(request):
    return render(request, 'index.html')


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
    return render(request, 'shop.html')


def info(request):
    return render(request, 'info.html')


def cart(request):
    return render(request, 'cart.html')


def logout(request):
    request.session.clear()
    response = redirect('index')
    response.delete_cookie('username')
    return response

def item(request):
    perfume = Perfume.objects.get(name='Bleu de Chanel')
    return render(request, 'item.html', {'perfume': perfume})
