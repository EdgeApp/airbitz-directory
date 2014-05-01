from django.contrib.gis.geos import Point, Polygon
from django.contrib.gis.measure import Distance
from django.core.cache import cache
from requests import Session, Request

import difflib
import math

from airbitz import settings

DEF_RADIUS=Distance(mi=100)
EARTHS_MEAN_RADIUS=6371000
DEG_TO_M=(EARTHS_MEAN_RADIUS * math.pi) / 180.0
HOP=Distance(mi=5)

def admin1Map(l):
    if l == 'GB':
        return 'UK'
    else:
        return l

def countryMap(c):
    return c

def locRound(loc, precision=3):
    """
    By rounding lat/lng we are able to better cache results. The following is a
    list of degrees to miles so we can see how precision would affect accuracy.

    Approximate value of a degree in miles
    Distance(m=1.0 * DEG_TO_M).mi    = 69.09332413987235
    Distance(m=0.1 * DEG_TO_M).mi    = 6.909332413987235
    Distance(m=0.01 * DEG_TO_M).mi   = 0.6909332413987235
    Distance(m=0.001 * DEG_TO_M).mi  = 0.06909332413987235
    Distance(m=0.0001 * DEG_TO_M).mi = 0.006909332413987235
    """
    l = loc.clone()
    l.x = round(l.x, precision)
    l.y = round(l.y, precision)
    return l

def locRoundedKey(loc):
    l = locRound(loc)
    return 'DEF_LOCS_{0}_{1}'.format(l.y, l.x)

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

def buildNearbyPoints(loc, steps=8):
    ps = []
    ps.append(loc)
    for i in range(1, steps):
        offset = (HOP.m / DEG_TO_M) * i
        p = loc.clone(); p.x = p.x + offset; ps.append(p)
        p = loc.clone(); p.y = p.y + offset; ps.append(p)
        p = loc.clone(); p.x = p.x - offset; ps.append(p)
        p = loc.clone(); p.y = p.y - offset; ps.append(p)
    return ps

def geocodeNearbyPoints(ps):
    rs, rm = [], {}
    for p in ps:
        r = googleNearby(p)
        if r and not rm.has_key(r):
            rs.append((p, r))
            rm[r] = 1
        if len(rs) > 4:
            break
    return rs

def nearbyPlaces(loc):
    key = locRoundedKey(loc)
    res = cache.get(key)
    if res:
        return res
    nloc = locRound(loc, precision=2)
    ps = buildNearbyPoints(nloc)
    rs = geocodeNearbyPoints(ps)
    rs.sort(lambda (p1, r1), (p2, r2): int(p1.distance(p2) * DEG_TO_M))
    rs = [r for p, r in rs]
    cache.set(key, rs, 60 * 60 * 24)
    return rs

def googleNearby(loc):
    rloc = locRound(loc)
    payload = {
        'sensor': 'false',
        'latlng': "{0},{1}".format(rloc.y, rloc.x), 
        'key': settings.GOOGLE_SERVER_KEY,
    }
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    res = cacheRequest(url, payload)
    if res.has_key('results') and len(res['results']) > 0:
        f = res['results'][0]
        m = populateComponents(f['address_components'])
        if m.has_key('locality') \
            and m.has_key('administrative_area_level_1') \
            and m.has_key('country'):
            return "{0}, {1}, {2}".format(m['locality']['long'],
                                        m['administrative_area_level_1']['short'],
                                        m['country']['long'])
    return None

def populateComponents(ls):
    m = {}
    for c in ls: 
        for t in c['types']:
            m[t] = {"short": c['short_name'], "long": c['long_name']}
    return m

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
    if details['result'].has_key('address_components'):
        admin = populateComponents(details['result']['address_components'])
    else:
        admin = {}
    # Expand bounding box
    # bounding = bounding.buffer(DEG_TO_M <= DEF_RADIUS.m) 
    return (point, bounding, admin)
