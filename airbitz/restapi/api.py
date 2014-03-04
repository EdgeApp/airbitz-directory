from django.contrib.gis.geos import Point, Polygon
from django.contrib.gis.measure import Distance
from haystack.query import SearchQuerySet, SQ
from haystack.inputs import Clean

import math
import logging
import subprocess

from directory.models import Business, Category
from location.models import OsmRelation

log=logging.getLogger("airbitz." + __name__)

DEF_POINT=Point((-117.124603, 33.028400))
DEF_RADIUS_M=Distance(mi=100).m
DEF_IP='24.152.191.12'
DEF_LOC_STR='San Francisco, CA'

EARTHS_MEAN_RADIUS=6371000
DEG_TO_M=(EARTHS_MEAN_RADIUS * math.pi) / 180.0

def autocompleteSerialize(row):
    if row.model.__name__ == 'Business':
        return { 'type': 'business', 'bizId': row.pk, 'text': row.content_auto }
    else:
        return { 'type': 'category', 'text': row.content_auto }

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
        print e
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
        self.point = DEF_POINT
        # Start by IP Lookup to find point
        if ip:
            self.point = processGeoIp(ip)
        if not self.point:
            self.point = DEF_POINT
        self.admin_level = 4
        if self.locationStr:
            self.filter_web_only = self.locationStr.lower() == 'web only'
            self.filter_on_web = self.locationStr.lower() == 'on the web'
            self.filter_current_location = self.locationStr.lower() == 'current location'
        else:
            self.filter_web_only = False
            self.filter_on_web = False
            self.filter_current_location = False
        if not self.isCurrentLocation() and not self.isOnWeb() and locationStr:
            sqs = SearchQuerySet().models(OsmRelation).filter(content_auto=locationStr)
            sqs = sqs[:1]
            if len(sqs) > 0:
                obj = sqs[0].object
                self.bounding = obj.geom
                if not self.bounding.contains(self.point):
                    self.point = obj.centroid
                    print 'Using centroid'
                else:
                    print 'NOT Using centroid'
                self.admin_level = obj.admin_level
        if ll:
            geoloc = parseGeoLocation(ll)
            if geoloc:
                if (self.bounding and self.bounding.contains(geoloc)) or not self.bounding:
                    self.point = geoloc;

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
        return self.location.point

    def isExactCategory(self, term):
        return Category.objects.filter(name=term).exists()

    def searchDirectory(self, term=None, geobounds=None, radius=None, category=None, sort=None):
        sqs = SearchQuerySet().models(Business)
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
            print 'got here....'
            sqs = sqs.order_by('-has_bitcoin_discount', '-score')
            sqs = sqs.load_all()
        else:
            sqs = sqs.distance('location', self.userLocation())
            sqs = sqs.order_by('distance')
            sqs = sqs.load_all()
            sqs = self.__geolocation_filter__(sqs, geobounds, radius)
        return [s.object for s in sqs]

    def __geolocation_filter__(self, sqs, geobounds, radius):
        geopoly = None
        if geobounds:
            geopoly = parseGeoBounds(geobounds)
        newsqs = []
        for s in sqs:
            s.object.distance = s.distance
            if s.location:
                if self.location.bounding and self.location.bounding.contains(s.location):
                    s.object.bounded = True
                    self.__append_if_within__(newsqs, s, geopoly)
                else:
                    newsqs.append(s)
        if geopoly or radius:
            newsqs2 = []
            for s in newsqs:
                if not s.location:
                    newsqs2.append(s)
                elif geopoly or radius:
                    loc = self.userLocation()
                    if geopoly and loc.distance(s.location) * DEG_TO_M <= DEF_RADIUS_M:
                        s.object.bounded = False
                        self.__append_if_within__(newsqs2, s, geopoly)
                    elif radius and loc.distance(s.location) * DEG_TO_M <= Distance(m=radius).m:
                        s.object.bounded = False
                        newsqs2.append(s)
            return newsqs2 
        else:
            return newsqs

    def __append_if_within__(self, ls, obj, poly):
        if poly:
            if poly.contains(obj.location):
                ls.append(obj)
        else:
            ls.append(obj)

    def autocompleteBusiness(self, term=None, location=None, geolocation=None):
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
        sqs = sqs.distance('location', self.userLocation())
        # XXX: sqs = sqs.dwithin('location', self.userLocation(), DEF_RADIUS_M)
        sqs = sqs.filter(fits).models(Business, Category)
        if self.location and self.location.bounding:
            sqs = self.boundSearchQuery(sqs, self.location)
        else:
            sqs = sqs[:10]
        return [autocompleteSerialize(result) for result in sqs]

    def boundSearchQuery(self, sqs, loc):
        newsqs = []
        for s in sqs:
            if s.model.__name__ == 'Business':
                if s.location and loc.bounding.contains(s.location):
                    newsqs.append(s)
            else:
                newsqs.append(s)
        return newsqs

    def autocompleteLocation(self, term=None):
        sqs = SearchQuerySet().models(OsmRelation)
        if term:
            formatted = wildcardFormat(term)
            sqs = sqs.filter(content_auto=formatted)
        sqs = sqs.distance('location', self.userLocation())
        # XXX: sqs = sqs.dwithin('location', self.userLocation(), DEF_RADIUS_M)
        sqs = sqs.order_by('distance')
        sqs = sqs[:10]
        return [result.content_auto for result in sqs]

    def querySetAddCategories(self, sqs, category):
        f = None
        for cterm in category.split(","):
            q = SQ(categories=cterm)
            if not f:
                f = q
            else:
                f = f | q
        return sqs.filter(f)

    def suggestNearText(self):
        point = self.userLocation()
        print point
        qs = OsmRelation.objects.filter(admin_level__lte=6).distance(point)\
                                .order_by('distance', '-admin_level')[:1]
        if len(qs) > 0:
            return "{0}".format(qs[0].name)
        elif self.location.ip:
            return ipToLocationString(self.location.ip)
        else:
            return DEF_LOC_STR


def getRequestIp(request):
    if request.META.has_key('HTTP_X_REAL_IP'):
        ip = request.META['HTTP_X_REAL_IP']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip

def ipToLocationString(ip):
    point = processGeoIp(ip)
    if point:
        try:
            rs = OsmRelation.objects.filter(admin_level__lte=6).distance(point)\
                                    .order_by('distance', '-admin_level')[:1]
            if rs:
                return "{0}".format(rs[0].name)
        except Exception as e:
            log.warn(e)
    return DEF_LOC_STR

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
        print e
        log.warn(e)
    return None

