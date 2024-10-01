from django.shortcuts import render
from django.db.models import Avg
from .models import Mountain, Route

def mountain_list(request):
    mountains = Mountain.objects.all()
    for mountain in mountains:
        mcs_avg = mountain.routes.aggregate(Avg('final_score'))['final_score__avg'] or 0
        mountain.mcs_average = round(mcs_avg, 2)
    return render(request, 'climbs/mountain_list.html', {'mountains': mountains})

def mountain_detail(request, pk):
    mountain = get_object_or_404(Mountain, pk=pk)
    # Calculate average final_score for all routes of this mountain
    mcs_average = mountain.routes.aggregate(Avg('final_score'))['final_score__avg'] or 0
    mcs_average = round(mcs_average, 2)
    return render(request, 'climbs/mountain_detail.html', {
        'mountain': mountain,
        'mcs_average': mcs_average,
    })

def route_detail(request, pk):
    route = get_object_or_404(Route, pk=pk)
    return render(request, 'climbs/route_detail.html', {'route': route})
