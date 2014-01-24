from django.contrib.gis.geos import Point, Polygon
from django.contrib.gis.measure import D
from django.db.models import Q
import logging
import subprocess

from directory.models import Business, GeoName, GeoNameZip

log=logging.getLogger("airbitz." + __name__)

# # Query San Diego bounding box
# http://localhost:8000/api/v1/search?query=Spi&bounds=32.7506,-117.2221|33.1709,-116.9041
# http://localhost:8000/api/v1/search?query=Spi&ll=32.7506,-117.2220
# 
# # Open street map equivalent
# http://openstreetmap.org/?minlon=-117.2221&minlat=32.7506&maxlon=-116.9041&maxlat=33.1709

RADIUS_DEFAULT=40000
DEFAULT_IP='24.152.191.12'

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
    qs = Business.objects.all()
    origin = None
    if term:
        qs = qs.filter(Q(name__icontains=term) | Q(description__icontains=term))
    if category:
        qs = qs.filter(category__name=category)
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
        qs.distance(origin)
    if sort == 0:
        qs = qs.order_by('has_bitcoin_discount', 'name')
    elif sort == 1 and origin:
        qs = qs.order_by('distance')
    print qs.query
    return qs

def autocompleteBusiness(term=None, location=None, geolocation=None):
    qs = Business.objects.none()
    if term:
        qs = Business.objects.filter(name__icontains=term)
    (qs, _) = querySetAddLocation(qs, location)
    (qs, _) = querySetAddGeoLocation(qs, geolocation)
    print qs.query
    return qs

# for f in autocompleteLocation('San D'): print f.admin_name2, f.admin_code1
# for f in autocompleteLocation('Califor'): print f.admin_name2, f.admin_code1
def autocompleteLocation(term=None, geolocation=None):
    if term:
        qs = GeoNameZip.objects.filter(Q(admin_name2__icontains=term)\
                                     | Q(admin_name1__icontains=term)\
                                     | Q(admin_code1__icontains=term))
        if geolocation:
            d = parseGeoLocation(geolocation)
            origin = Point((d['lon'], d['lat']))
            qs = qs.distance(origin).order_by('distance')
        qs = qs.distinct('admin_code1', 'admin_name2')
        return qs
    else:
        return GeoNameZip.objects.none()

def querySetAddLocation(qs, location):
    d = parseLocationString(location)
    #if d['county']:
    #    qs = qs.filter(city=d['county'])
    if d['state']:
        qs = qs.filter(state=d['state'])
    if d['country']:
        qs = qs.filter(country=d['country'])
    if d['postalcode']:
        qs = qs.filter(postalcode=d['postalcode'])
    return (qs, d)

def querySetAddGeoLocation(qs, geolocation, radius=RADIUS_DEFAULT):
    origin = None
    if geolocation:
        d = parseGeoLocation(geolocation)
        origin = Point(d['lon'], d['lat'])
        if radius:
            qs = qs.filter(center__distance_lt=(origin, D(m=radius)))
    return (qs, origin)

def suggestNearText(ip, geolocation=None):
    if geolocation:
        d = parseGeoLocation(geolocation)
        origin = Point((d['lon'], d['lat']))
        qs = GeoName.objects.all().distance(origin).order_by('distance')[1]
        if qs:
            return qs[0].place_name, qs[0].admin_name1, qs[0].country
        else:
            return processGeoIp(ip)
    else:
        return processGeoIp(ip)


# TODO: this function needs a lot of work and a lot of testing
#   parseLocationString('   Oceanside, CA')
#   parseLocationString('  California   ')
#   parseLocationString(' San Diego, CA,   92127     ')
#   parseLocationString('OR') == parseLocationString('Oregon')
def parseLocationString(location):
    d = {
        'city': None,
        'country': None,
        'postalcode': None,
        'county': None,
        'state': None,
        'point': None,
    }
    if not location:
        return d
    values = map(lambda x : x.strip(), location.split(","))
    values.reverse()
    for v in values:
        v = v.strip()
        if not d['postalcode']:
            r = GeoNameZip.objects.filter(postalcode=v)[:1]
            if r:
                d['postalcode'] = r[0].postalcode
                d['city'] = r[0].place_name
                d['county'] = r[0].admin_name2
                d['state'] = r[0].admin_code1
                d['country'] = r[0].country
                d['point'] = Point(r[0].center.y, r[0].center.x)
                continue
        if not d['state']:
            r = GeoNameZip.objects.filter(Q(admin_code1=v) | Q(admin_name1=v))[:1]
            if r:
                d['state'] = r[0].admin_code1
                d['country'] = r[0].country
                continue
        if not d['county']:
            r = GeoNameZip.objects.filter(Q(admin_code2=v) | Q(admin_name2=v))[:1]
            if r:
                d['city'] = r[0].place_name
                d['county'] = r[0].admin_name2
                d['state'] = r[0].admin_code1
                d['point'] = Point(r[0].center.y, r[0].center.x)
                d['country'] = r[0].country
                continue
        if not d['city']:
            r = GeoNameZip.objects.filter(place_name=v)[:1]
            if r:
                d['city'] = r[0].place_name
                d['county'] = r[0].admin_name2
                d['state'] = r[0].admin_code1
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
    return DEFAULT_IP
    
def processGeoCounty(row):
    try:
        v = row.strip().split(",")
        lat, lon = float(v[4]), float(v[5])
        origin = Point(lon, lat)
        rs = GeoNameZip.objects.all().distance(origin).order_by('distance')[:1]
        if rs:
            return "{0}, {1}".format(rs[0].admin_name2, rs[0].admin_code1)
    except Exception as e:
        log.warn(e)
    return None

