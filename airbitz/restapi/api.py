from django.contrib.gis.geos import Point, Polygon
from django.contrib.gis.measure import Distance
from django.core.cache import cache
from haystack.inputs import Clean
from haystack.query import SearchQuerySet, SQ
from requests import Session, Request

import difflib
import logging
import math
import subprocess

from airbitz import settings
from directory.models import Business, Category

log=logging.getLogger("airbitz." + __name__)

DEF_SRID=4326
DEF_COUNTRY="US"
DEF_POINT=Point((-117.124603, 33.028400))
DEF_RADIUS=Distance(mi=100)
DEF_IP='24.152.191.12'
DEF_LOC_STR='San Francisco, CA'

CURRENT_LOCATION='Current Location'

EARTHS_MEAN_RADIUS=6371000
DEG_TO_M=(EARTHS_MEAN_RADIUS * math.pi) / 180.0

def cacheRequest(url, params):
    s = Session()
    req = Request('GET', url, params=params)
    prepped = req.prepare()
    res = cache.get(prepped.url)
    if res:
        return res
    else:
        res = s.send(prepped).json()
        cache.set(prepped.url, res, 60 * 60)
        return res

def googleBestMatch(txt, loc=None):
    res = googleAutocomplete(txt, loc)
    if len(res['predictions']) == 0:
        return None
    ls = []
    for row in res['predictions']:
        ratio = difflib.SequenceMatcher(None, row['description'], txt).ratio()
        ls.append((ratio, row))
    # Sort desc by accuracy 1 is perfect match
    ls.sort(lambda (x1, x2), (y1, y2): int(y1 * 100) - int(x1 * 100))
    # Return most accurate
    return ls[0][1]

def googleNearby(loc):
    payload = {
        'sensor': 'false',
        'latlng': "{0},{1}".format(loc.y, loc.x), 
        'key': settings.GOOGLE_SERVER_KEY,
    }
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    res = cacheRequest(url, payload)
    if res.has_key('results'):
        f = res['results'][0]
        m = {}
        for c in f['address_components']:
            for t in c['types']:
                m[t] = {"short": c['short_name'], "long": c['long_name']}
    if m.has_key('locality') \
        and m.has_key('administrative_area_level_1') \
        and m.has_key('country'):
        return "{0}, {1}, {2}".format(m['locality']['long'],
                                      m['administrative_area_level_1']['short'],
                                      m['country']['long'])
    return None

def googleAutocomplete(txt, loc=None, filtered=True):
    payload = {
        'sensor': 'false',
        'input': txt, 
        'types': '(regions)',
        'key': settings.GOOGLE_SERVER_KEY,
    }
    if loc:
        payload['location'] = "{0},{1}".format(loc.y, loc.x)
        payload['radius'] = "50000" # Max google search radius
    url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json'
    return cacheRequest(url, payload)

def googlePlaceDetails(ref):
    payload = {
        'reference': ref,
        'sensor': 'false',
        'key': settings.GOOGLE_SERVER_KEY
    }
    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    return cacheRequest(url, payload)

def googleDetailsToBounding(ref):
    details = googlePlaceDetails(ref)
    loc = details['result']['geometry']['location']
    point = Point((loc['lng'], loc['lat']))
    viewport = details['result']['geometry']['viewport']
    sw = viewport['southwest']
    ne = viewport['northeast']
    box = {
        'minlat': float(sw['lat']),
        'minlon': float(sw['lng']),
        'maxlat': float(ne['lat']),
        'maxlon': float(ne['lng']),
    }
    bounding = Polygon.from_bbox((box['minlon'], box['minlat'], box['maxlon'], box['maxlat']))
    # Expand bounding box
    bounding = bounding.buffer(DEG_TO_M <= DEF_RADIUS.m) 
    return (point, bounding)

def autocompleteSerialize(row):
    if row.model.__name__ == 'Business':
        return { 'type': 'business', 'bizId': row.pk, 'text': row.content_auto }
    else:
        return { 'type': 'category', 'text': row.content_auto }

def autocompleteSuggSerialize(row, used):
    res = []
    if not used.has_key(row.content_auto):
        used[row.content_auto] = True
        res.append({ 'type': 'business', 'bizId': row.pk, 'text': row.content_auto })

    for c in row.categories:
        if used.has_key(c):
            continue
        used[c] = True
        res.append({ 'type': 'category', 'text': c })
        return res
    return res

def flatten(ls):
    return [item for sublist in ls for item in sublist]

def wildcardFormat(term):
    return WildCard(term)

def parseGeoLocation(ll):
    vals = ll.split(",")
    try:
        return Point(float(vals[1]), float(vals[0]))
    except Exception as e:
        log.warn(e)
        raise AirbitzApiException('Unable to parse geographic location.')

def parseGeoBounds(bounds):
    if not bounds:
        return None
    try:
        (sw,ne) = bounds.split("|")
        sw = sw.split(",")
        ne = ne.split(",")
        box = {
            'minlat': float(sw[0]),
            'minlon': float(sw[1]),
            'maxlat': float(ne[0]),
            'maxlon': float(ne[1]),
        }
        return Polygon.from_bbox((box['minlon'], box['minlat'], box['maxlon'], box['maxlat']))
    except Exception as e:
        log.warn(e)
        raise AirbitzApiException('Unable to parse geographic bounds.')

class WildCard(Clean):
    input_type_name = 'wildcard'
    post_process = True

    def __init__(self, query_string, **kwargs):
        self.original = query_string
        super(WildCard, self).__init__(query_string, **kwargs)

    def prepare(self, query_obj):
        query_string = self.query_string.replace(',', '')
        qs = ''
        query_string = query_string.strip()
        a = query_string.split(' ')
        for i,q in enumerate(a):
            q = q.strip()
            if not q:
                continue
            if i == len(a) - 1:
                qs += q + '*'
            else:
                qs += q + '~0.8 '
        return qs.strip()

class AirbitzApiException(BaseException):
    pass

def toInt(request, key, default):
    try:
        if request.QUERY_PARAMS.has_key(key):
            return int(request.QUERY_PARAMS.get(key, None))
    except Exception as e:
        log.warn(e)
        raise AirbitzApiException('Unable to handle request. Error with {0} format.'.format(key))
    return default

class Location(object):
    """ Takes location data and determines bounding box 
        and centroid to use during the searches 
        """
    def __init__(self, locationStr=None, ll=None, ip=None):
        self.ip = ip
        self.locationStr = locationStr
        self.bounding = None
        self.sortPoint = DEF_POINT
        self.userPoint = DEF_POINT
        self.userCountry = DEF_COUNTRY
        # Start by IP Lookup to find point
        if ip:
            self.sortPoint = processGeoIp(ip)
            self.userPoint = self.sortPoint
        if not self.sortPoint:
            self.sortPoint = DEF_POINT
            self.userPoint = DEF_POINT
            self.userCountry = DEF_COUNTRY
        self.admin_level = 4
        if self.locationStr:
            self.filter_web_only = self.locationStr.lower() == 'web only'
            self.filter_on_web = self.locationStr.lower() == 'on the web'
            self.filter_current_location = self.locationStr.lower() == CURRENT_LOCATION.lower()
        else:
            self.filter_web_only = False
            self.filter_on_web = False
            self.filter_current_location = False
        if self.isOnWeb():
            pass
        if not self.isCurrentLocation() and not self.isOnWeb() and locationStr:
            res = googleBestMatch(locationStr, self.userPoint)
            if res:
                ref = res['reference']
                (centroid, bounding) = googleDetailsToBounding(ref)
                self.bounding = bounding
                if not self.boundingContains(self.sortPoint):
                    self.sortPoint = centroid
        if ll:
            geoloc = parseGeoLocation(ll)
            if geoloc:
                self.userPoint = geoloc;
                if not self.bounding or self.boundingContains(geoloc):
                    self.sortPoint = geoloc;

    @property
    def hasBounding(self):
        return self.bounding is not None

    def boundingContains(self, location):
        if not self.hasBounding:
            return False
        if self.bounding.contains(location):
            return True
        return False

    def boundingExpandedContains(self, location):
        if not self.hasBounding:
            return False
        if self.bounding.distance(location) * DEG_TO_M <= DEF_RADIUS.m:
            return True
        return False


    def isWebOnly(self):
        return self.filter_web_only

    def isOnWeb(self):
        return self.filter_on_web

    def isCurrentLocation(self):
        return self.filter_current_location

class ApiProcess(object):
    def __init__(self, locationStr=None, ll=None, ip=None):
        self.location = Location(locationStr=locationStr, ll=ll, ip=ip)

    def userLocation(self):
        return self.location.sortPoint

    def isExactCategory(self, term):
        if term:
            return Category.objects.filter(name__iexact=term).exists()
        else: 
            return False

    def searchDirectory(self, term=None, geobounds=None, radius=None, category=None, sort=None):
        sqs = SearchQuerySet().models(Business)
        geopoly = parseGeoBounds(geobounds)
        if term:
            formatted = wildcardFormat(term)
            sqs = sqs.filter(SQ(categories=term) 
                           | SQ(name=term) 
                           | SQ(name=formatted) 
                           | SQ(description=term))
        if category:
            sqs = self.querySetAddCategories(sqs, category)
        if self.isExactCategory(term):
            sqs = sqs.filter(categories=term)
        if self.location.isWebOnly():
            sqs = sqs.filter(SQ(has_online_business=True) & SQ(has_physical_business=False))
        elif self.location.isOnWeb():
            sqs = sqs.filter(SQ(has_online_business=True))
        if self.location.isOnWeb():
            if not term:
                sqs = sqs.order_by('-has_bitcoin_discount', '-score')
            else:
                sqs = sqs.order_by('-score')
            sqs = sqs.load_all()
            sqs = self.__filer_on_web__(sqs)
        else:
            sqs = sqs.filter(SQ(has_physical_business=True))
            sqs = sqs.distance('location', self.userLocation())
            sqs = sqs.order_by('distance')
            sqs = sqs.load_all()
            sqs = self.__geolocation_filter__(sqs, geopoly, radius)
        return [s.object for s in sqs]

    def __filer_on_web__(self, sqs):
        inCountry = []
        outCountry = []
        for s in sqs:
            if s.object.country == self.location.userCountry:
                inCountry.append(s)
            else:
                outCountry.append(s)
        return inCountry + outCountry

    def __geolocation_filter__(self, sqs, geopoly, radius):
        newsqs = []
        if self.location.hasBounding:
            # Do we have a bounding box?
            for s in sqs:
                s.object.distance = s.distance
                s.object.bounded = False
                if s.location:
                    s.object.distance = Distance(m=s.location.distance(self.location.userPoint) * DEG_TO_M)
                    s.object.sortDistance = Distance(m=s.location.distance(self.location.sortPoint) * DEG_TO_M)
                    if self.location.boundingContains(s.location):
                        # Its within the bounding box 
                        s.object.bounded = True
                        self.__append_if_within__(newsqs, s, poly=geopoly, radius=radius)
                    elif self.location.boundingExpandedContains(s.location):
                        # Outside of bounding, but within the DEF_RADIUS
                        self.__append_if_within__(newsqs, s, poly=geopoly, radius=radius)
            return newsqs
        else:
            if not radius:
                radius = DEF_RADIUS.m
            for s in sqs:
                s.object.distance = s.distance
                s.object.bounded = False
                if s.location:
                    s.object.distance = Distance(m=s.location.distance(self.location.userPoint) * DEG_TO_M)
                    s.object.sortDistance = Distance(m=s.location.distance(self.location.sortPoint) * DEG_TO_M)
                    self.__append_if_within__(newsqs, s, poly=geopoly, radius=radius)
            return newsqs

    def __append_if_within__(self, ls, obj, poly=None, radius=None):
        if poly:
            if poly.contains(obj.location):
                ls.append(obj)
        elif radius:
            if obj.object.sortDistance.m < radius:
                ls.append(obj)
        else:
            ls.append(obj)

    def autocompleteBusiness(self, term=None, location=None, geolocation=None):
        if not term:
            return self.suggestNearCategories()

        sqs = SearchQuerySet()
        if term:
            formatted = wildcardFormat(term)
            sqs = sqs.filter(content_auto=formatted)
        if location: 
            fits = SQ(django_ct='directory.business')
            if self.location.isWebOnly():
                fits = fits & SQ(has_online_business=True) & SQ(has_physical_business=False)
            elif self.location.isOnWeb():
                fits = fits & SQ(has_online_business=True)
        else:
            fits = SQ(django_ct='directory.business')
        fits = (fits) | SQ(django_ct='directory.category')
        sqs = sqs.filter(fits).models(Business, Category)
        if self.location.isOnWeb() or self.location.isWebOnly():
            sqs = sqs.order_by('-has_bitcoin_discount')
        else:
            if self.location and self.location.bounding:
                sqs = self.boundSearchQuery(sqs, self.location)
            # if self.userLocation():
            #     sqs = sqs.distance('location', self.userLocation())
            #     sqs = sqs.dwithin('location', self.userLocation(), DEF_RADIUS)
        sqs = sqs[:10]
        return [autocompleteSerialize(result) for result in sqs]

    def boundSearchQuery(self, sqs, loc):
        newsqs = []
        for s in sqs:
            if s.model.__name__ == 'Business':
                if loc.bounding and s.location and loc.bounding.contains(s.location):
                    newsqs.append(s)
            else:
                newsqs.append(s)
        return newsqs

    def autocompleteLocation(self, term=None):
        res = googleAutocomplete(term, self.userLocation())
        return [r['description'] for r in res['predictions']]

    def querySetAddCategories(self, sqs, category):
        f = None
        for cterm in category.split(","):
            q = SQ(categories=cterm)
            if not f:
                f = q
            else:
                f = f | q
        return sqs.filter(f)

    def suggestNearCategories(self):
        sqs = SearchQuerySet().models(Business)
        if self.location.isWebOnly():
            sqs = sqs.filter(has_online_business=True, has_physical_business=False)
            sqs = sqs.order_by('-has_bitcoin_discount')
        elif self.location.isOnWeb():
            sqs = sqs.filter(has_online_business=True)
            sqs = sqs.order_by('-has_bitcoin_discount')
        else:
            sqs = sqs.filter(has_physical_business=True)
            sqs = sqs.distance('location', self.userLocation())
            sqs = sqs.order_by('distance')

        if self.location and self.location.bounding:
            sqs = self.boundSearchQuery(sqs, self.location)

        used = {}
        sqs = flatten([autocompleteSuggSerialize(s, used) for s in sqs])
        return filter(lambda x : x is not None, sqs)[:10]

    def suggestNearText(self):
        point = self.userLocation()
        nearText = nearTextFromPoint(point)
        if nearText:
            return nearText
        elif self.location.ip:
            return ipToLocationString(self.location.ip)
        else:
            return DEF_LOC_STR

def getRequestIp(request):
    return request.META['REMOTE_ADDR']

def ipToLocationString(ip):
    point = processGeoIp(ip)
    if point:
        return nearTextFromPoint(point)
    return DEF_LOC_STR

def nearTextFromPoint(point):
    try:
        return googleNearby(point)
    except Exception as e:
        log.warn(e)
    return None

def processGeoIp(ip):
    if ip in ("10.0.2.2", "127.0.0.1"):
        ip = localToPublicIp()
    proc = subprocess.Popen(['geoiplookup', ip], stdout=subprocess.PIPE)
    data = proc.stdout.read()
    for line in data.split('\n'):
        row = line.split(':')
        if len(row) == 2:
            data = None
            (k, v) = (row[0], row[1])
            if k.__contains__("City"):
                data = processRow(v)
            if data:
                return data
    return None

def localToPublicIp():
    """ This should only be called during development """
    URL='http://www.networksecuritytoolkit.org/nst/tools/ip.php'
    try:
        import urllib
        return urllib.urlopen(URL).read().strip()
    except:
        log.warn('unable to look up ip')
    # Just return a default IP
    return DEF_IP
    
def processRow(row):
    try:
        v = row.strip().split(",")
        lat, lon = float(v[4]), float(v[5])
        return Point(lon, lat)
    except Exception as e:
        try:
            lat, lon = float(v[5]), float(v[6])
            return Point(lon, lat)
        except:
            log.warn(e)
    return None

