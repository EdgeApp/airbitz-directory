from django.http import Http404
from django.contrib.gis.measure import D
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from directory.models import Business, BusinessImage
from airbitz.settings import GOOGLE_MAP_KEY
from restapi import api

SEARCH_LIMIT = 20
DISTANCE_LIMIT_KILOMETERS = 20

def get_biz(request, *args, **kwargs):
    biz = get_object_or_404(Business, **kwargs)
    if request.user.is_superuser or biz.status == 'PUB':
        return biz
    else:
        raise Http404

def landing(request):
    context = { }
    return render_to_response('landing.html', RequestContext(request, context))

def business_search(request):
    term = request.GET.get('term', None)
    ll = request.GET.get('ll', None)
    near = request.GET.get('near', None)
    results = api.searchDirectory(term=term, location=near, geolocation=ll)
    context = {
        'results': results[:20],
        'mapkey': GOOGLE_MAP_KEY
    }
    return render_to_response('search.html', RequestContext(request, context))

def business_info(request, bizId):
    biz = get_biz(request, pk=bizId)
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

