import datetime
from django.contrib.gis.measure import D
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from urllib import urlencode
import urllib
from airbitz import regions_data
from airbitz.regions_data import ACTIVE_REGIONS, ALL_REGIONS

from airbitz.settings import GOOGLE_MAP_KEY
from directory.models import Business, BusinessImage
# from management.views import isManager
from restapi import api
from directory.models import STATUS_CHOICES, SOCIAL_TYPES

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
        'all_regions': ALL_REGIONS,
        'biz_total': Business.objects.filter(status="PUB", country__in=regions_data.get_active_country_codes()).count(),
    }
    return render_to_response('home.html', RequestContext(request, context))

def business_search(request, arg_term=None, arg_category=None, arg_location=None, arg_ll=None):
    if arg_term:
        term = arg_term
    else:
        term = request.GET.get('term', None)
    if arg_category:
        category = arg_category
    else:
        category = request.GET.get('category', None)
    if arg_ll:
        ll = arg_ll
    else:
        ll = request.GET.get('ll', None)
    if arg_location:
        location = arg_location
    else:
        location = request.GET.get('location', None)

    ip = api.getRequestIp(request)
    a = api.ApiProcess(locationStr=location, ll=ll, ip=ip)
    results = a.searchDirectory(term=term, category=category)

    if not results:
        return redirect('search_no_results')


    request.session['nearText'] = location
    if location == 'On the Web':
        results_per_page = 30
    else:
        results_per_page = 25

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

        # RELATED: REMOVING REGION MAP
        # 'active_regions': ACTIVE_REGIONS,
        # 'all_regions': ALL_REGIONS,

    }
    return render_to_response('search.html', RequestContext(request, context))


def business_search_no_results(request):
    context = {}
    return render_to_response('search-no-results.html', RequestContext(request, context))

def business_info(request, bizId):
    biz = get_biz(request, pk=bizId)
    imgs = BusinessImage.objects.filter(business=biz)

    nearby = []
    if biz.center:
        nearby = Business.objects.filter(status='PUB').filter(\
                    ~Q(pk=biz.id), \
                    center__distance_lt=(biz.center, D(km=DISTANCE_LIMIT_KILOMETERS)))
        nearby = nearby.distance(biz.center).order_by('distance')[:12]
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


def add_business(request, url=None):

    context = {
        'STATUS_CHOICES': STATUS_CHOICES,
        'SOCIAL_TYPES': SOCIAL_TYPES,
        'starter_url': url,
        'top_bg_img': '',
    }
    return render_to_response('business_add.html', RequestContext(request, context))




# handles email redirects for desktop or android gmail
def redirect_blf(request):

    address = request.GET['address']
    url = 'bitcoin:' + address
    # print '\n------------------------------------\n'
    # print 'ADDRESS:', address
    # print 'URL BUILT:', url
    # print '\n------------------------------------\n'
    response = HttpResponse("", status=302)
    response['Location'] = str(url)
    return response


def btc_email_request(request):
    context = {}
    return render_to_response('btc-email-request.html', RequestContext(request, context))

def email_request_template(request):
    context = {}
    return render_to_response('template-email-request.html', RequestContext(request, context))


# app download fallback page
def app_download(request):
    context = {}
    return render_to_response('app-download.html')
