from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os
from django.conf import settings

def generar_pdf_alumno(alumno):
    """Genera un PDF con los datos del alumno"""
    
    # Crear directorio temporal si no existe
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    # Ruta del archivo PDF
    pdf_path = os.path.join(temp_dir, f'alumno_{alumno.id}.pdf')
    
    # Crear el documento PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Título
    title = Paragraph('Datos del Alumno', title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Datos del alumno en tabla
    data = [
        ['Campo', 'Información'],
        ['Nombre Completo', alumno.nombre_completo],
        ['Email', alumno.email],
        ['Teléfono', alumno.telefono or 'No especificado'],
        ['Fecha de Nacimiento', alumno.fecha_nacimiento.strftime('%d/%m/%Y')],
        ['Dirección', alumno.direccion],
        ['Fecha de Registro', alumno.fecha_registro.strftime('%d/%m/%Y %H:%M')],
    ]
    
    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
    ]))
    
    elements.append(table)
    
    # Construir PDF
    doc.build(elements)
    
    return pdf_path