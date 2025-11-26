from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ScraperForm
from .utils import buscar_articulos_educativos

@login_required
def scraper_view(request):
    resultados = []
    
    if request.method == 'POST':
        form = ScraperForm(request.POST)
        if form.is_valid():
            palabra_clave = form.cleaned_data['palabra_clave']
            
            try:
                resultados = buscar_articulos_educativos(palabra_clave)
                
                if resultados:
                    messages.success(request, f'Se encontraron {len(resultados)} resultados para "{palabra_clave}"')
                    
                    # Enviar resultados por email
                    if request.POST.get('enviar_email'):
                        email_body = f'Resultados de búsqueda para: {palabra_clave}\n\n'
                        for i, resultado in enumerate(resultados, 1):
                            email_body += f"{i}. {resultado['titulo']}\n"
                            email_body += f"   URL: {resultado['url']}\n"
                            email_body += f"   Descripción: {resultado['descripcion']}\n\n"
                        
                        try:
                            send_mail(
                                subject=f'Resultados de búsqueda: {palabra_clave}',
                                message=email_body,
                                from_email=settings.DEFAULT_FROM_EMAIL,
                                recipient_list=[request.user.email],
                                fail_silently=False,
                            )
                            messages.success(request, f'Resultados enviados a {request.user.email}')
                        except Exception as e:
                            messages.error(request, f'Error al enviar email: {str(e)}')
                else:
                    messages.warning(request, 'No se encontraron resultados')
                    
            except Exception as e:
                messages.error(request, f'Error en la búsqueda: {str(e)}')
    else:
        form = ScraperForm()
    
    return render(request, 'scraper/scraper.html', {
        'form': form,
        'resultados': resultados
    })