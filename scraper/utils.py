import requests
from bs4 import BeautifulSoup
import time

def buscar_articulos_educativos(palabra_clave):
    """
    Realiza scraping de Wikipedia para buscar artículos relacionados
    """
    resultados = []
    
    try:
        # Buscar en Wikipedia en español
        url = f"https://es.wikipedia.org/wiki/{palabra_clave.replace(' ', '_')}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Obtener título principal
            titulo = soup.find('h1', {'id': 'firstHeading'})
            if titulo:
                titulo_text = titulo.get_text()
                
                # Obtener primer párrafo
                contenido = soup.find('div', {'id': 'mw-content-text'})
                primer_parrafo = ''
                if contenido:
                    parrafos = contenido.find_all('p', limit=3)
                    for p in parrafos:
                        texto = p.get_text().strip()
                        if len(texto) > 50:
                            primer_parrafo = texto[:300] + '...'
                            break
                
                resultados.append({
                    'titulo': titulo_text,
                    'url': url,
                    'descripcion': primer_parrafo or 'Sin descripción disponible'
                })
        
        # Buscar artículos relacionados (simulado con búsqueda adicional)
        search_url = f"https://es.wikipedia.org/w/index.php?search={palabra_clave}"
        response_search = requests.get(search_url, headers=headers, timeout=10)
        
        if response_search.status_code == 200:
            soup_search = BeautifulSoup(response_search.content, 'html.parser')
            resultados_busqueda = soup_search.find_all('div', {'class': 'mw-search-result-heading'}, limit=5)
            
            for resultado in resultados_busqueda:
                link = resultado.find('a')
                if link:
                    titulo_rel = link.get_text()
                    url_rel = 'https://es.wikipedia.org' + link.get('href')
                    
                    # Obtener descripción del resultado
                    parent = resultado.find_parent('li')
                    descripcion_elem = parent.find('div', {'class': 'searchresult'})
                    descripcion = descripcion_elem.get_text()[:200] + '...' if descripcion_elem else 'Sin descripción'
                    
                    resultados.append({
                        'titulo': titulo_rel,
                        'url': url_rel,
                        'descripcion': descripcion
                    })
        
        # Limitar a 10 resultados
        return resultados[:10]
        
    except Exception as e:
        print(f"Error en scraping: {str(e)}")
        return []