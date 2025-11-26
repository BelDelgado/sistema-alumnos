from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Alumno
from .forms import AlumnoForm
from .utils import generar_pdf_alumno
import os

@login_required
def dashboard(request):
    alumnos = Alumno.objects.filter(usuario=request.user)
    return render(request, 'alumnos/dashboard.html', {'alumnos': alumnos})

@login_required
def crear_alumno(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.usuario = request.user
            alumno.save()
            messages.success(request, f'Alumno {alumno.nombre_completo} creado exitosamente.')
            return redirect('alumnos:dashboard')
    else:
        form = AlumnoForm()
    
    return render(request, 'alumnos/crear_alumno.html', {'form': form})

@login_required
def editar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            messages.success(request, f'Alumno {alumno.nombre_completo} actualizado exitosamente.')
            return redirect('alumnos:dashboard')
    else:
        form = AlumnoForm(instance=alumno)
    
    return render(request, 'alumnos/editar_alumno.html', {'form': form, 'alumno': alumno})

@login_required
def eliminar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        nombre = alumno.nombre_completo
        alumno.delete()
        messages.success(request, f'Alumno {nombre} eliminado exitosamente.')
        return redirect('alumnos:dashboard')
    
    return render(request, 'alumnos/eliminar_alumno.html', {'alumno': alumno})

@login_required
def enviar_pdf_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)
    
    try:
        # Generar PDF
        pdf_path = generar_pdf_alumno(alumno)
        
        # Enviar por email
        email = EmailMessage(
            subject=f'Datos del Alumno: {alumno.nombre_completo}',
            body=f'Adjunto encontrarás el PDF con los datos del alumno {alumno.nombre_completo}.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[request.user.email],
        )
        
        with open(pdf_path, 'rb') as pdf_file:
            email.attach(f'alumno_{alumno.id}.pdf', pdf_file.read(), 'application/pdf')
        
        email.send()
        
        # Eliminar archivo temporal
        os.remove(pdf_path)
        
        messages.success(request, f'PDF enviado exitosamente a {request.user.email}')
    except Exception as e:
        messages.error(request, f'Error al enviar el PDF: {str(e)}')
    
    return redirect('alumnos:dashboard')