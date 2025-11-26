from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegistroForm, LoginForm

def registro_view(request):
    if request.user.is_authenticated:
        return redirect('alumnos:dashboard')
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Enviar email de bienvenida
            try:
                send_mail(
                    subject='¡Bienvenido al Sistema de Gestión de Alumnos!',
                    message=f'Hola {user.username},\n\nTu cuenta ha sido creada exitosamente.\n\n¡Bienvenido a nuestra plataforma!',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                messages.success(request, f'Cuenta creada exitosamente. Se ha enviado un correo de bienvenida a {user.email}')
            except Exception as e:
                messages.warning(request, f'Cuenta creada, pero no se pudo enviar el correo: {str(e)}')
            
            login(request, user)
            return redirect('alumnos:dashboard')
    else:
        form = RegistroForm()
    
    return render(request, 'accounts/registro.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('alumnos:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {username}!')
                return redirect('alumnos:dashboard')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('accounts:login')