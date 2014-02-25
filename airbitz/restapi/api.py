from django.contrib.gis.geos import Point, Polygon
# from haystack.inputs import AltParser
from haystack.query import SearchQuerySet, SQ
from haystack.inputs import Clean

import logging
import subprocess

from directory.models import Business, Category
from location.models import GeoNameZip, OsmRelation

log=logging.getLogger("airbitz." + __name__)

DEFAULT_POINT=Point((-117.124603, 33.028400))
DEFAULT_RADIUS=40000
DEFAULT_IP='24.152.191.12'
DEFAULT_LOC_STRING='San Francisco, CA'

def autocompleteSerialize(row):
    if row.model.__name__ == 'Business':
        return { 'type': 'business', 'bizId': row.pk, 'text': row.content_auto }
    else:
        return { 'type': 'category', 'text': row.content_auto }

def wildcardFormat(term):
    return WildCard(term)

def isWebOnly(location):
    return location.lower() == 'web only'

def isOnWebOnly(location):
    return location.lower() == 'on the web'

def isCurrentLocation(location):
    return location.lower() == 'current location'


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
    def __init__(self, location):
        self.location = location
        self.bounding = None
        self.point = DEFAULT_POINT
        if self.location:
            self.filter_web_only = self.location.lower() == 'web only'
            self.filter_on_web = self.location.lower() == 'on the web'
            self.filter_current_location =  self.location.lower() == 'current location'
        else:
            self.filter_web_only = False
            self.filter_on_web = False
            self.filter_current_location = False

    def isWebOnly(self):
        return self.filter_web_only

    def isOnWebOnly(self):
        return self.filter_on_web

    def isCurrentLocation(self):
        return self.filter_current_location

class ApiProcess(object):
    def __init__(self):
        self.point = DEFAULT_POINT

    def userLocation(self):
        return self.point

    def searchDirectory(self, term=None, location=None, geolocation=None, 
                        geobounds=None, radius=None, category=None, sort=0):
        sqs = SearchQuerySet().models(Business)
        if term:
            formatted = wildcardFormat(term)
            sqs = sqs.filter(SQ(categories=term) 
                           | SQ(categories=formatted) 
                           | SQ(name=term) 
                           | SQ(name=formatted) 
                           | SQ(description=term))
        sqs = self.searchAddGeoLocation(sqs, geolocation)
        sqs = self.querySetAddCategories(sqs, category)
        l = self.parseLocationString(location)
        if l.isCurrentLocation():
            pass
        elif l.isWebOnly():
            sqs = sqs.filter(SQ(has_online_business=True) & SQ(has_physical_business=False))
        elif l.isOnWebOnly():
            sqs = sqs.filter(SQ(has_online_business=True))
        sqs = sqs.distance('location', self.userLocation())
        if sort == 0:
            sqs = sqs.order_by('-has_bitcoin_discount', 'name')
        elif sort == 1:
            sqs = sqs.order_by('distance')
        if geobounds:
            d = self.parseGeoBounds(geobounds)
            l.bounding = Polygon.from_bbox((d['minlon'], d['minlat'], d['maxlon'], d['maxlat']))
        if l and l.bounding:
            sqs = self.boundSearchQuery(sqs, l)

        ids = [s.pk for s in sqs]
        newqs = Business.objects.filter(pk__in=ids).distance(self.userLocation())
        return newqs

    def autocompleteBusiness(self, term=None, location=None, geolocation=None):
        sqs = SearchQuerySet()
        l = self.parseLocationString(location)
        if term:
            formatted = wildcardFormat(term)
            sqs = sqs.filter(content_auto=formatted)
        if location: 
            fits = SQ(django_ct='directory.business')
            if l.isCurrentLocation():
                pass
            elif l.isWebOnly():
                fits = fits & SQ(has_online_business=True) & SQ(has_physical_business=False)
            elif l.isOnWebOnly():
                fits = fits & SQ(has_online_business=True)
        else:
            fits = SQ(django_ct='directory.business')
        fits = (fits) | SQ(django_ct='directory.category')
        sqs = self.searchAddGeoLocation(sqs, geolocation)
        sqs = sqs.filter(fits).models(Business, Category)
        if l and l.bounding:
            sqs = self.boundSearchQuery(sqs, l)
        else:
            sqs = sqs[:10]
        return [autocompleteSerialize(result) for result in sqs]

    def boundSearchQuery(self, sqs, l):
        newsqs = []
        for s in sqs:
            if s.model.__name__ == 'Business':
                if s.location and l.bounding.contains(s.location):
                    newsqs.append(s)
            else:
                newsqs.append(s)
        return newsqs

    def autocompleteLocation(self, term=None, geolocation=None, ip=None):
        sqs = SearchQuerySet().models(OsmRelation)
        if term:
            formatted = wildcardFormat(term)
            sqs = sqs.filter(content_auto=formatted)
        sqs = self.searchAddGeoLocation(sqs, geolocation)
        sqs = sqs.order_by('distance')
        sqs = sqs[:10]
        return [result.content_auto for result in sqs]

    def querySetAddCategories(self, sqs, category):
        if not category:
            return sqs
        f = None
        for cterm in category.split(","):
            q = SQ(categories=cterm)
            if not f:
                f = q
            else:
                f = f | q
        return sqs.filter(f)

    def searchAddGeoLocation(self, sqs, geolocation):
        if geolocation:
            d = parseGeoLocation(geolocation)
            origin = Point(d['lon'], d['lat'])
            return sqs.distance('location', origin)
        else:
            return sqs.distance('location', self.userLocation())

    def parseLocationString(self, location):
        l = Location(location)
        if not location:
            return l
        if l.isCurrentLocation() or l.isOnWebOnly() or l.isWebOnly():
            return l

        formatted = wildcardFormat(location)
        sqs = SearchQuerySet().models(OsmRelation).filter(content_auto=formatted)
        sqs = sqs.distance('location', self.userLocation()).order_by('distance')[:1]
        if len(sqs) > 0:
            obj = sqs[0].object
            l.bounding = obj.geom
            l.point = obj.centroid
        return l

def getRequestIp(request):
    if request.META.has_key('HTTP_X_REAL_IP'):
        ip = request.META['HTTP_X_REAL_IP']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip

def suggestNearByRequest(request, geolocation=None):
    ip = getRequestIp(request)
    return suggestNearText(ip, geolocation)

def suggestNearText(ip, geolocation=None):
    if geolocation:
        d = parseGeoLocation(geolocation)
        origin = Point((d['lon'], d['lat']))
        qs = GeoNameZip.objects.all().distance(origin).order_by('distance')[:1]
        if len(qs) > 0:
            return "{0}, {1}".format(qs[0].admin_name2, qs[0].admin_code1)
        else:
            return processGeoIp(ip)
    else:
        return processGeoIp(ip)

def parseGeoLocation(ll):
    vals = ll.split(",")
    try:
        return {
            'lat': float(vals[0]),
            'lon': float(vals[1])
        }
    except Exception as e:
        log.warn(e)
        raise AirbitzApiException('Unable to parse geographic location.')

def parseGeoBounds(bounds):
    try:
        (sw,ne) = bounds.split("|")
        sw = sw.split(",")
        ne = ne.split(",")
        return {
            'minlat': float(sw[0]),
            'minlon': float(sw[1]),
            'maxlat': float(ne[0]),
            'maxlon': float(ne[1]),
        }
    except Exception as e:
        log.warn(e)
        raise AirbitzApiException('Unable to parse geographic bounds.')

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
                data = processGeoCounty(v)
            if data:
                return data
    return DEFAULT_LOC_STRING

def localToPublicIp():
    """ This should only be called during development """
    URL='http://www.networksecuritytoolkit.org/nst/tools/ip.php'
    try:
        import urllib
        return urllib.urlopen(URL).read().strip()
    except:
        log.warn('unable to look up ip')
    # Just return a default IP
    return DEFAULT_IP
    
def processGeoCounty(row):
    try:
        v = row.strip().split(",")
        lat, lon = float(v[4]), float(v[5])
        origin = Point(lon, lat)
        print origin
        rs = GeoNameZip.objects.all().distance(origin).order_by('distance')[:1]
        if rs:
            s = "{0}, {1}".format(rs[0].admin_name2, rs[0].admin_code1)
            print s
            return s
    except Exception as e:
        print e
        log.warn(e)
    return None

