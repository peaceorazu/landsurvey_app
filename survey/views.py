from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import SurveyEntry
from io import BytesIO
from django.db.models import Sum
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

DROPDOWNS = [
    'Trenching S1 Normal soil (1.2m)', 'Trenching S2 Hard soil (1m)',
    'Trenching S3 Soft Rock (0.5m)', 'Trenching S4 Hard Rock (0.5m)',
    'T/boring [Soil Road, Entrance] (PVC/HDPE)',
    'T/boring [Asp Road, F.S] (GI Pipe)',
    'Alphalt Cutting', 'Bridge/Culvert (PVC/HDPE)',
    'Bridge/Culvert (GI Pipe)', 'Swampy Area',
    'Erosion Area', 'Railay Crossing'
]

def landing_page(request):
    return render(request, 'landing.html')



def index(request):
    if request.method == 'POST':
        request.session['state'] = request.POST.get('state')
        request.session['segment_id'] = request.POST.get('segment_id')
        request.session['route_id'] = request.POST.get('route_id')
        return redirect('input_form')
    return render(request, 'index.html')

def input_form(request):
    # Ensure session data exists
    if not all(key in request.session for key in ['state', 'segment_id', 'route_id']):
        return redirect('index')
    
    if request.method == 'POST':
        try:
            SurveyEntry.objects.create(
                state=request.session['state'],
                segment_id=request.session['segment_id'],
                route_id=request.session['route_id'],
                category=request.POST.get('category'),
                value=float(request.POST.get('value')),
            )
        except (ValueError, TypeError):
            # Handle invalid number input
            pass
    
    # Change created_at to timestamp
    values = SurveyEntry.objects.filter(
        segment_id=request.session.get('segment_id', '')
    ).order_by('-timestamp')  # Changed from created_at to timestamp
    
    return render(request, 'input_form.html', {
        'dropdowns': DROPDOWNS,
        'values': values
    })

def export_pdf(request):
    entries = SurveyEntry.objects.filter(
        segment_id=request.session.get('segment_id', '')
    ).order_by('-timestamp')
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "Survey Report")
    
    # Table Data
    data = [["Category", "Value", "Timestamp"]]
    for entry in entries:
        data.append([
            entry.category,
            str(entry.value),
            entry.timestamp.strftime("%Y-%m-%d %H:%M")
        ])
    
    # Create table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2e7d32')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    
    table.wrapOn(p, 400, 600)
    table.drawOn(p, 100, 600)
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

def summary(request):
    if 'segment_id' not in request.session:
        return redirect('index')
    
    entries = SurveyEntry.objects.filter(
        segment_id=request.session['segment_id']
    )
    totals = entries.values('category').annotate(total=Sum('value'))
    
    return render(request, 'summary.html', {
        'totals': totals,
        'session_data': {
            'state': request.session.get('state'),
            'segment_id': request.session.get('segment_id'),
            'route_id': request.session.get('route_id')
        }
    })