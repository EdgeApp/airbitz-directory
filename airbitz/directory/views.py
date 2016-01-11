import datetime
from django.contrib.gis.measure import D
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from airbitz import regions_data
from airbitz.regions_data import ACTIVE_REGIONS, ALL_REGIONS
from airbitz.settings import GOOGLE_MAP_KEY
from directory.utils import mailchimp_list_signup
from directory.models import Business, BusinessImage, SocialId
from directory.models import STATUS_CHOICES, SOCIAL_TYPES
from directory.team_info import TEAM_INFO
from directory.applications_info import APPLICATIONS_INFO
from restapi import api
from restapi.serializers import calc_distance

SEARCH_LIMIT = 20
DISTANCE_LIMIT_KILOMETERS = 20
SPECIALS_TAG='Bitcoin Bowl'

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
    # print 'QUERY ARGS:', args
    # print 'QUERY KWARGS:', kwargs
    biz = get_object_or_404(Business, **kwargs)
    # print biz

    if request.user.is_superuser or biz.status == 'PUB':
        return biz
    else:
        raise Http404

def home_v2(request):
    return render_to_response('home-v2.html', RequestContext(request, {}))



def get_team_info():
    # set up team info rows for mobile and desktop
    team_id_sm_row_1 = ['paul', 'tim']
    team_id_sm_row_2 = ['william', 'lucas']
    team_id_sm_row_3 = ['will','mk']
    team_id_sm_row_4 = ['rj','nik']
    team_id_lg_row_1 = ['paul', 'tim', 'william','lucas']
    team_id_lg_row_2 = ['will','mk', 'rj', 'nik']

    # initialize 8 empty list variables
    team_info_sm_row_1, team_info_sm_row_2, team_info_sm_row_3, team_info_sm_row_4, \
    team_info_lg_row_1, team_info_lg_row_2 = ([] for i in range(6))

    for profile in TEAM_INFO:
        if profile['id'] in team_id_sm_row_1:
            team_info_sm_row_1.append(profile)
        if profile['id'] in team_id_sm_row_2:
            team_info_sm_row_2.append(profile)
        if profile['id'] in team_id_sm_row_3:
            team_info_sm_row_3.append(profile)
        if profile['id'] in team_id_sm_row_4:
            team_info_sm_row_4.append(profile)

        if profile['id'] in team_id_lg_row_1:
            team_info_lg_row_1.append(profile)
        if profile['id'] in team_id_lg_row_2:
            team_info_lg_row_2.append(profile)

    team_info = {}
    team_info.update({'sm-1': team_info_sm_row_1})
    team_info.update({'sm-2': team_info_sm_row_2})
    team_info.update({'sm-3': team_info_sm_row_3})
    team_info.update({'sm-4': team_info_sm_row_4})
    team_info.update({'lg-1': team_info_lg_row_1})
    team_info.update({'lg-2': team_info_lg_row_2})

    return team_info


def landing_v2(request):
    if request.POST.get('signup_type') == 'mailchimp':
        mailchimp_list_signup(request)

    team_info = get_team_info()
    
    context = {
        'active_regions': ACTIVE_REGIONS,
        'team_info_sm_row_1': team_info['sm-1'],
        'team_info_sm_row_2': team_info['sm-2'],
        'team_info_sm_row_3': team_info['sm-3'],
        'team_info_sm_row_4': team_info['sm-4'],
        'team_info_lg_row_1': team_info['lg-1'],
        'team_info_lg_row_2': team_info['lg-2'],
        'team_info': TEAM_INFO,
        'applications_info': APPLICATIONS_INFO,
        # 'all_regions': ALL_REGIONS,
        # 'biz_total': Business.objects.filter(status="PUB", country__in=regions_data.get_active_country_codes()).count(),
    }
    return render_to_response('landing_v2.html', RequestContext(request, context))


def landing(request):
    print 'OLD LANDING'
    context = {
        'active_regions': ACTIVE_REGIONS,
        'all_regions': ALL_REGIONS,
        'biz_total': Business.objects.filter(status="PUB", country__in=regions_data.get_active_country_codes()).count(),
    }
    return render_to_response('home.html', RequestContext(request, context))

def __business_search__(request, action, arg_term=None, arg_category=None, arg_location=None, 
                        arg_ll=None, template='search.html'):
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
    results = a.searchDirectory(term=term, category=category, show_hidden=False)

    if not results:
        return business_search_no_results(request, action) 

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
    # populate missing fields from DB
    ids = []
    for r in results:
        ids.append(r.pk)
    bizs = dict([(str(b.pk), b) for b in Business.objects.filter(id__in=ids)])
    for r in results:
        biz = bizs[r.pk]
        r.has_bitcoin_discount = biz.has_bitcoin_discount
        r.get_absolute_url = biz.get_absolute_url()
        r.center = biz.center
        r.gmap_directions_url = biz.gmap_directions_url
        r.social = SocialId.objects.filter(business=biz)
        r.landing_image = biz.landing_image
        r.mobile_landing_image = biz.mobile_landing_image
        r.categories = biz.categories
        try:
            r.distance = calc_distance(a.userLocation(), biz.center)
        except Exception as e:
            print e

    context = {
        'search_action': action,
        'results': results,
        'mapkey': GOOGLE_MAP_KEY,
        'userLocation': a.userLocation(),
        'searchLocation': a.location,
        'was_search': True,
        'page_obj': paginator.page(page_num),
        'results_info': results_info,
        'form_action': '/blackfriday',

        # RELATED: REMOVING REGION MAP
        # 'active_regions': ACTIVE_REGIONS,
        # 'all_regions': ALL_REGIONS,
    }
    return render_to_response(template, RequestContext(request, context))

def business_search(request, *args, **kwargs):
    return __business_search__(request, reverse('search'), *args, **kwargs)

def blackfriday(request, **kwargs):
    kwargs['arg_category'] = SPECIALS_TAG
    kwargs['template'] = 'specials.html'
    return __business_search__(request, reverse('blackfriday'), **kwargs)


def business_search_no_results(request, action):
    context = {
        'search_action': action
    }
    return render_to_response('search-no-results.html', RequestContext(request, context))

def business_info(request, biz_id=None, biz_slug=None):

    biz = get_biz(request, pk=biz_id)

    if biz.status == 'PUB':
        if not biz_slug == biz.slug:
            return HttpResponsePermanentRedirect(biz.get_absolute_url())

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

def email_request_template_android(request):
    context = {}
    return render_to_response('template-email-request_android.html', RequestContext(request, context))


# app download fallback page
def app_download(request):
    return render_to_response('app-download.html')
