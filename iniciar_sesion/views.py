from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CustomAuthenticationForm


def signin(request):
    try:
        if request.method == 'GET':
            return render(request, 'signin.html', {
                'form': CustomAuthenticationForm
            })
        else:
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
    
    except Exception as e:
        print(f"Se produjo un error al iniciar sesión: {str(e)}")
        return redirect('signin')


def signout(request):
    try:
        logout(request)
        return redirect('signin')
    
    except Exception as e:
        print(f"Se produjo un error al cerrar sesión: {str(e)}")
        return redirect('home')