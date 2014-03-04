from django.contrib.auth.decorators import user_passes_test
from django.contrib.gis.measure import D
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from airbitz.settings import GOOGLE_MAP_KEY
from directory.models import Business, BusinessImage
# from management.views import isManager
from restapi import api

SEARCH_LIMIT = 20
DISTANCE_LIMIT_KILOMETERS = 20


WEEKDAYS = (
    ('sunday', 'Sun'),
    ('monday', 'Mon'),
    ('tuesday', 'Tue'),
    ('wednesday', 'Wed'),
    ('thursday', 'Thu'),
    ('friday', 'Fri'),
    ('saturday', 'Sat'),
)


def get_biz_hours(biz):
    days_hours = biz.businesshours_set.all()

    week_of_hours = {}

    for weekday in WEEKDAYS:
        # print weekday[0], weekday[1]
        week_of_hours[weekday[1]] = ''

        for dh in days_hours:
            if dh.dayOfWeek == weekday[0]:
                # matched on the day of week so add the hours to that dict key
                week_of_hours[weekday[1]] = [dh.hourStart, dh.hourEnd]

    return week_of_hours

def get_biz(request, *args, **kwargs):
    biz = get_object_or_404(Business, **kwargs)
    if request.user.is_superuser or biz.status == 'PUB':
        return biz
    else:
        raise Http404

COMING_SOON='/coming_soon'

def isAllowed(user):
    return user.is_authenticated()

def coming_soon(request):
    return render_to_response('coming_soon.html', RequestContext(request, {}))

@user_passes_test(isAllowed, login_url=COMING_SOON, redirect_field_name=None)
def landing(request):
    return render_to_response('landing.html', RequestContext(request, {}))

@user_passes_test(isAllowed, login_url=COMING_SOON, redirect_field_name=None)
def business_search(request):
    term = request.GET.get('term', None)
    category = request.GET.get('category', None)
    ll = request.GET.get('ll', None)
    location = request.GET.get('location', None)
    ip = api.getRequestIp(request)
    a = api.ApiProcess(locationStr=location, ll=ll, ip=ip)
    results = a.searchDirectory(term=term, category=category)

    request.session['nearText'] = location
    paginator = Paginator(results, 10)
    print 'PAGE RANGE', paginator.page_range

    if request.GET.get('page'):
        page = request.GET.get('page')
    else:
        page = 1

    results = paginator.page(page)

    context = {
        'results': results,
        'mapkey': GOOGLE_MAP_KEY,
        'userLocation': a.userLocation(),
        'searchLocation': a.location,
        'was_search': True,
        'page_obj': paginator.page(page)
    }
    return render_to_response('search.html', RequestContext(request, context))

@user_passes_test(isAllowed, login_url=COMING_SOON, redirect_field_name=None)
def business_info(request, bizId):
    biz = get_biz(request, pk=bizId)
    imgs = BusinessImage.objects.filter(business=biz)

    nearby = []
    if biz.center:
        nearby = Business.objects.filter(status='PUB').filter(\
                    ~Q(pk=biz.id), \
                    center__distance_lt=(biz.center, D(km=DISTANCE_LIMIT_KILOMETERS)))
        nearby = nearby.distance(biz.center).order_by('distance')[:6]
    context = {
        'biz': biz,
        'imgs': imgs,
        'results': nearby,
        'mapkey': GOOGLE_MAP_KEY,
        'biz_hours': get_biz_hours(biz),
        'weekdays': WEEKDAYS,
        'was_search': False
    }
    return render_to_response('business_info.html', RequestContext(request, context))

