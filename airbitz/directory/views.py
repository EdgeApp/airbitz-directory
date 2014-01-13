from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from directory.models import Business, BusinessImage
from airbitz.settings import GOOGLE_MAP_KEY

SEARCH_LIMIT = 20
DISTANCE_LIMIT_KILOMETERS = 20

def landing(request):
    context = { }
    return render_to_response('landing.html', RequestContext(request, context))

def business_search(request):
    results = Business.objects.all()
    q = request.GET.get('q', None)
    lat = request.GET.get('lat', None)
    lon = request.GET.get('lon', None)
    near = request.GET.get('near', None)
    results = Business.objects.all()
    if not q and not near:
        results = []
    else:
        if q:
            results = results.filter(name__icontains=q)
        if near:
            results = results.filter(postalcode=near)
        if lat and lon:
            origin = Point((float(lon), float(lat)))
            results = results.distance(origin).order_by('distance')
        
    context = {
        'results': results[:20],
        'mapkey': GOOGLE_MAP_KEY
    }
    return render_to_response('search.html', RequestContext(request, context))

def business_info(request, bizId):
    biz = get_object_or_404(Business, pk=bizId)
    imgs = BusinessImage.objects.filter(business=biz)

    nearby = []
    if biz.center:
        nearby = Business.objects.filter(\
                    ~Q(pk=biz.id), \
                    center__distance_lt=(biz.center, D(km=DISTANCE_LIMIT_KILOMETERS)))
        nearby = nearby.distance(biz.center).order_by('distance')[:4]
    context = {
        'biz': biz,
        'imgs': imgs,
        'nearby': nearby,
        'mapkey': GOOGLE_MAP_KEY
    }
    return render_to_response('business_info.html', RequestContext(request, context))

