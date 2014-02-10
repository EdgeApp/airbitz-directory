from django.contrib.gis.geos import Point, Polygon
from django.contrib.gis.measure import D
from django.db.models import Q
from haystack.query import SearchQuerySet
from haystack.query import SQ
import logging
import subprocess

from directory.models import Business, Category
from location.models import GeoNameZip, LocationString

log=logging.getLogger("airbitz." + __name__)

# # Query San Diego bounding box
# http://localhost:8000/api/v1/search?query=Spi&bounds=32.7506,-117.2221|33.1709,-116.9041
# http://localhost:8000/api/v1/search?query=Spi&ll=32.7506,-117.2220
# 
# # Open street map equivalent
# http://openstreetmap.org/?minlon=-117.2221&minlat=32.7506&maxlon=-116.9041&maxlat=33.1709

DEFAULT_POINT=Point((-117.124603, 33.028400))
RADIUS_DEFAULT=40000
DEFAULT_IP='24.152.191.12'
DEFAULT_LOC_STRING='San Francisco, CA'

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
        

def searchDirectory(term=None, location=None, \
                    geolocation=None, geobounds=None, \
                    radius=None, category=None, sort=0):
    qs = Business.objects.filter(status='PUB')
    origin = None
    if term:
        qs = qs.filter(Q(name__icontains=term)
                     | Q(description__icontains=term)
                     | Q(categories__name__icontains=term))
    if category:
        f = None
        for cterm in category.split(","):
            q = Q(categories__name=cterm)
            if not f:
                f = q
            else:
                f = f | q
        qs = qs.filter(f)
    (qs, dloc) = querySetAddLocation(qs, location)
    if dloc['point']:
        origin = dloc['point']
    (qs, lloc) = querySetAddGeoLocation(qs, geolocation, radius=radius)
    if lloc:
        origin = lloc
    if geobounds:
        d = parseGeoBounds(geobounds)
        geom = Polygon.from_bbox((d['minlon'], d['minlat'], d['maxlon'], d['maxlat']))
        qs = qs.filter(center__contained=geom)
    if origin:
        qs = qs.distance(origin)
    if sort == 0:
        qs = qs.order_by('has_bitcoin_discount', 'name')
    elif sort == 1 and origin:
        qs = qs.order_by('distance')
    return qs

def autocompleteBusiness(term=None, location=None, geolocation=None):
    sqs = SearchQuerySet()
    if term:
        sqs = sqs.filter(content_auto=term)
    if location: 
        fits = SQ(django_ct='directory.business')
        d = parseLocationString(location)
        if d['admin2_name']:
            fits = fits & (SQ(admin2_name=d['admin2_name'])
                         | SQ(admin3_name=d['admin2_name']))
        if d['admin1_code']:
            fits = fits & SQ(admin1_code=d['admin1_code'])
        if d['country']:
            fits = fits & SQ(country=d['country'])
    else:
        fits = SQ(django_ct='directory.business')
    fits = (fits) | SQ(django_ct='directory.category')
    sqs = searchAddGeoLocation(sqs, geolocation)
    sqs = sqs.filter(fits).models(Business, Category)
    return [autocompleteSerialize(result) for result in sqs]

def autocompleteSerialize(row):
    if row.model.__name__ == 'Business':
        return { 'type': 'business', 'bizId': row.pk, 'text': row.content_auto }
    else:
        return { 'type': 'category', 'text': row.content_auto }

def autocompleteLocation(term=None, geolocation=None, ip=None):
    if term:
        sqs = SearchQuerySet().models(LocationString).autocomplete(content_auto=term)
        sqs = searchAddGeoLocation(sqs, geolocation)
        sqs = sqs[:10]
        return [result.content_auto for result in sqs]
    else:
        return []

def searchAddGeoLocation(sqs, geolocation):
    if geolocation:
        return sqs.distance('center', geolocation).order_by('distance')
    else:
        # XXX: Biased this to san diego, need to bias by IP
        return sqs.distance('location', DEFAULT_POINT).order_by('distance')

def querySetAddLocation(qs, location):
    d = parseLocationString(location)
    if not d['country'] \
            and not d['admin1_code'] \
            and not d['admin2_name'] \
            and not ['admin3_name']:
        # If no country found, then return empty results
        qs = qs.filter(pk=0)
        return (qs, d)
    if d['admin2_name']:
        qs = qs.filter(Q(admin2_name=d['admin2_name']) 
                     | Q(admin3_name=d['admin2_name']))
    if d['admin1_code']:
        qs = qs.filter(admin1_code=d['admin1_code'])
    if d['country']:
        qs = qs.filter(country=d['country'])
    if d['postalcode']:
        qs = qs.filter(postalcode=d['postalcode'])
    return (qs, d)

def querySetAddGeoLocation(qs, geolocation, radius=RADIUS_DEFAULT):
    radius = max(radius, 1)
    origin = None
    if geolocation:
        d = parseGeoLocation(geolocation)
        origin = Point(d['lon'], d['lat'])
        if radius:
            qs = qs.filter(center__distance_lt=(origin, D(m=radius)))
    return (qs, origin)

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

def parseLocationString(location):
    d = {
        'admin1_code': None,
        'admin2_name': None,
        'admin3_name': None,
        'country': None,
        'point': None,
        'postalcode': None,
    }
    if not location:
        return d

    sqs = SearchQuerySet().autocomplete(content_auto=location)
    sqs = sqs.distance('location', DEFAULT_POINT).order_by('distance')[:1]
    if len(sqs) > 0:
        d['admin1_code'] = sqs[0].admin1_code
        d['admin2_name'] = sqs[0].admin2_name
        d['country'] = sqs[0].country_code
    else:
        values = map(lambda x : x.strip(), location.split(","))
        values.reverse()
        for v in values:
            v = v.strip()
            if not d['postalcode']:
                r = GeoNameZip.objects.filter(postalcode=v)[:1]
                if r:
                    d['postalcode'] = r[0].postalcode
                    d['admin3_name'] = r[0].place_name
                    d['admin2_name'] = r[0].admin_name2
                    d['admin1_code'] = r[0].admin_code1
                    d['country'] = r[0].country
                    d['point'] = Point(r[0].center.y, r[0].center.x)
                    continue
            if not d['admin1_code']:
                r = GeoNameZip.objects.filter(Q(admin_code1=v) | Q(admin_name1=v))[:1]
                if r:
                    d['admin1_code'] = r[0].admin_code1
                    d['country'] = r[0].country
                    continue
            if not d['admin2_name']:
                r = GeoNameZip.objects.filter(Q(admin_code2=v) | Q(admin_name2=v))[:1]
                if r:
                    d['admin3_name'] = r[0].place_name
                    d['admin2_name'] = r[0].admin_name2
                    d['admin1_code'] = r[0].admin_code1
                    d['point'] = Point(r[0].center.y, r[0].center.x)
                    d['country'] = r[0].country
                    continue
            if not d['admin3_name']:
                r = GeoNameZip.objects.filter(place_name=v)[:1]
                if r:
                    d['admin3_name'] = r[0].place_name
                    d['admin2_name'] = r[0].admin_name2
                    d['admin1_code'] = r[0].admin_code1
                    d['point'] = Point(r[0].center.y, r[0].center.x)
                    d['country'] = r[0].country
                    continue
    return d

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

