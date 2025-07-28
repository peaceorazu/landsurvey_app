from django.shortcuts import render, redirect
from .models import SurveyEntry
from django.db.models import Sum

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
                value=float(request.POST.get('value'))
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