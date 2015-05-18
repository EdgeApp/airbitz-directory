from restapi import api
import logging
import settings
from regions_data import get_active_regions_list


log=logging.getLogger(__name__)

def near(request):
    nearText = None
    if request.GET.has_key('location'):
        nearText = request.GET.get('location', None) or api.CURRENT_LOCATION
    else:
        nearText = request.session.get('nearText', None) 
        if not nearText: 
            ip = api.getRequestIp(request)
            a = api.ApiProcess(ip=ip)
            nearText = a.suggestNearText()
    request.session['nearText'] = nearText
    return { 'location': nearText }


def debug(request):
    return {
        'DEBUG': settings.DEBUG,
    }

def active_regions(request):
    return {
        'us_active_regions_list':               get_active_regions_list('US-'),
        'ca_active_regions_list':               get_active_regions_list('CA-'),
        'south_america_active_regions_list':    get_active_regions_list('SOUTHAMERICA'),
        'eu_active_regions_list':               get_active_regions_list('EUROPE'),
        'asia_active_regions_list':             get_active_regions_list('ASIA'),
        'southeast_asia_active_regions_list':   get_active_regions_list('SOUTHEAST_ASIA'),
        'oceana_active_regions_list':           get_active_regions_list('OCEANA'),
    }

# SEO RELATED
def get_canonical(request):
    path = request.get_full_path()

    url = settings.CANONICAL_BASE + path

    return {
            'canonical': url
    }
