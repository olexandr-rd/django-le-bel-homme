from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    return render(request, 'index.html')


def shop(request):
    return render(request, 'shop.html')


def info(request):
    return render(request, 'info.html')


def cart(request):
    return render(request, 'cart.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == 'oleksa' and password == 'password':
            request.session['username'] = username
            response = redirect('index')
            response.set_cookie('username', username)
            return response
        else:
            return HttpResponse('Помилка в імені чи паролі')
    else:
        return render(request, 'login.html')


def logout(request):
    request.session.clear()
    response = redirect('index')
    response.delete_cookie('username')
    return response


def item(request):
    return render(request, 'item.html')
