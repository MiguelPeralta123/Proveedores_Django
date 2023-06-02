from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CustomAuthenticationForm


def signin(request):
    # Si accedemos con POST, enviamos los valores de los input a '/signin'
    if request.method == 'POST':
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': CustomAuthenticationForm,
                'error': 'Email y/o contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('home')
    # Si accedemos a la página de login con GET, devolvemos el formulario
    else:
        return render(request, 'signin.html', {
            'form': CustomAuthenticationForm
        })


def signout(request):
    logout(request)
    return redirect('signin')
