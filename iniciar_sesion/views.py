from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CustomAuthenticationForm, CustomRegistrationForm


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


def signup(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Display a message saying that the user was created
            return redirect('settings')
        else:
            # Display a message saying that the user was not created
            error = 'Error al crear el usuario. Intente de nuevo.'
            return render(request, 'signup.html', {
                'form': form,
                'error': error,
            })
            
    else:
        form = CustomRegistrationForm()

    return render(request, 'signup.html', {
        'form': form,
    })