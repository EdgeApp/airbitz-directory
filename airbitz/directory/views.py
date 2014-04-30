import datetime
from django.contrib.gis.measure import D
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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

# ISO_3166 Region codes http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
# these correspond to jvectormaps
ACTIVE_REGIONS = {
    'US-CA': {'name': 'California',
              'search': 'California, United States'},
    'US-TX': {'name': 'Texas',
              'search': 'Texas, United States'},
    'US-NY': {'name': 'New York',
              'search': 'New York, United States'},
    'US-HI': {'name': 'Hawaii',
              'search': 'Hawaii, United States'},
    'US-NJ': {'name': 'New Jersey',
              'search': 'New Jersey, United States'},
    'US-GA': {'name': 'Georgia',
              'search': 'Georgia, United States'},
    'US-IL': {'name': 'Illinois',
              'search': 'Illinois, United States'},
    'US-UT': {'name': 'Utah',
              'search': 'Utah, United States'},
    'US-NV': {'name': 'Nevada',
              'search': 'Nevada, United States'},
    'US-CO': {'name': 'Colorado',
              'search': 'Colorado, United States'},
    'US-FL': {'name': 'Florida',
              'search': 'Florida, United States'},
    'US-NH': {'name': 'New Hampshire',
              'search': 'New Hapshire, United States'},
    'US-MA': {'name': 'Massachusetts',
              'search': 'Massachusetts, United States'},
    'US-VT': {'name': 'Vermont',
              'search': 'Vermont, United States'},
    'US-PA': {'name': 'Pennsylvania',
              'search': 'Pennsylvania, United States'},
    'US-CT': {'name': 'Connecticut',
              'search': 'Connecticut, United States'},
    'US-DE': {'name': 'Delaware',
              'search': 'Delaware, United States'},
    'US-MD': {'name': 'Maryland',
              'search': 'Maryland, United States'},
    'US-WA': {'name': 'Washington',
              'search': 'Washington, United States'},
    'US-OR': {'name': 'Oregon',
              'search': 'Oregon, United States'},
    'US-AK': {'name': 'Alaska',
              'search': 'Alaska, United States'},
    'US-AZ': {'name': 'Arizona',
              'search': 'Arizona, United States'},
    'US-NM': {'name': 'New Mexico',
              'search': 'New Mexico, United States'},
    'US-MI': {'name': 'Michigan',
              'search': 'Michigan, United States'},
    'US-MN': {'name': 'Minnesota',
              'search': 'Minnesota, United States'},
    'US-DC': {'name': 'Washington DC',
              'search': 'Washington, DC, United States'},
    'US-IN': {'name': 'Indiana',
              'search': 'Indiana, United States'},
    'US-IA': {'name': 'Iowa',
              'search': 'Iowa, United States'},
    'US-KS': {'name': 'Kansas',
              'search': 'Kansas, United States'},
    'US-WY': {'name': 'Wyoming',
              'search': 'Wyoming, United States'},

    'CA-ON': {'name': 'Ontario',
              'search': 'Ontario, Canada'},
    'CA-BC': {'name': 'British Columbia',
              'search': 'Ontario, Canada'},
    'CA-QC': {'name': 'Quebec',
              'search': 'Quebec, Canada'},

    'NL': {'name': 'Netherlands',
           'search': 'Netherlands'},


}



def get_biz_hours(biz):
    days_hours = biz.businesshours_set.all()
    midnight = datetime.time(0,0,0)
    week_of_hours = {}

    for weekday in WEEKDAYS:
        week_of_hours[weekday[1]] = ''

        for dh in days_hours:
            if dh.dayOfWeek == weekday[0]: # matched on the day of week so add the hours to that dict key
                if (dh.hourStart == midnight and dh.hourEnd == None) \
                    or (dh.hourStart == None and dh.hourEnd == None): # if matched this day was open 24hr
                    week_of_hours[weekday[1]] = ['Open 24hr', None]
                else:
                    week_of_hours[weekday[1]] = [dh.hourStart, dh.hourEnd]

    return week_of_hours

def get_biz(request, *args, **kwargs):
    biz = get_object_or_404(Business, **kwargs)
    if request.user.is_superuser or biz.status == 'PUB':
        return biz
    else:
        raise Http404

def home_v2(request):
    return render_to_response('home-v2.html', RequestContext(request, {}))

def landing(request):
    context = {
        'active_regions': ACTIVE_REGIONS,
    }
    return render_to_response('home.html', RequestContext(request, context))

def business_search(request):
    term = request.GET.get('term', None)
    category = request.GET.get('category', None)
    ll = request.GET.get('ll', None)
    location = request.GET.get('location', None)
    ip = api.getRequestIp(request)
    a = api.ApiProcess(locationStr=location, ll=ll, ip=ip)
    results = a.searchDirectory(term=term, category=category)

    request.session['nearText'] = location
    if location == 'On the Web':
        results_per_page = 30
    else:
        results_per_page = 10

    paginator = Paginator(results, results_per_page)

    page = request.GET.get('page')
    try:
        results = paginator.page(page)
        page_num = int(page)
    except PageNotAnInteger:
        page_num = 1
        results = paginator.page(page_num)
    except EmptyPage:
        page_num = paginator.num_pages
        results = paginator.page(page_num)

    results_left = min(paginator.count, results_per_page, 
                       (paginator.count - results_per_page * (page_num - 1)))
    results_info = {
        'total': paginator.count,
        'results_left': results_left,
        'results_per_page': results_per_page
    }

    context = {
        'results': results,
        'mapkey': GOOGLE_MAP_KEY,
        'userLocation': a.userLocation(),
        'searchLocation': a.location,
        'was_search': True,
        'page_obj': paginator.page(page_num),
        'results_info': results_info,
        'active_regions': ACTIVE_REGIONS,
    }
    return render_to_response('search.html', RequestContext(request, context))


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
        'was_search': False,
    }
    return render_to_response('business_info.html', RequestContext(request, context))

