# -*- coding: utf-8 -*-

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.core.cache import cache
from haystack.inputs import Clean
from haystack.query import SearchQuerySet, SQ
from haystack.utils.geo import D

import logging
import subprocess

from directory.models import Business, BusinessImage, Category
from airbitz.region_definitions import ALL_COUNTRY_LABELS
import locapi
import json

log=logging.getLogger("airbitz." + __name__)

DEF_LANG='en'
DEF_SRID=4326
DEF_COUNTRY="US"
DEF_POINT=Point((-117.124603, 33.028400))
DEF_IP='24.152.191.12'
DEF_LOC_STR='United States'

CURRENT_LOCATION='current location'
CUR_LOC_ARRAY=[CURRENT_LOCATION, 'ubicación actual']
WEB_LOC_ARRAY=['on the web', 'en la red']
WEB_ONLY_ARRAY=['web only']
LOCKED_USERS = [35, 39] # rackwallet and coinsource

def autocompleteSerialize(row, lang=DEF_LANG):
    if row.model.__name__ == 'Business':
        image = json.loads(row.landing_image_json)
        if image.has_key('thumbnail'):
            thumbnail = image['thumbnail']
        else:
            thumbnail = None
        return { 'type': 'business', 'bizId': row.pk, 'text': row.content_auto, 'square_image': thumbnail }
    else:
        if not ApiProcess.isSupportedLang(lang) or lang == DEF_LANG:
            return { 'type': 'category', 'text': row.text }
        else:
            return { 'type': 'category', 'text': getattr(row, lang + '_text') }

def autocompleteSuggSerialize(row, used, lang=DEF_LANG):
    res = []
    if not used.has_key(row.content_auto):
        used[row.content_auto] = True
        res.append({ 'type': 'business', 'bizId': row.pk, 'text': row.content_auto })
    if not ApiProcess.isSupportedLang(lang) or lang == DEF_LANG:
        cats = row.categories
    else:
        cats = getattr(row, lang + '_categories')
    if cats:
        for c in cats:
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

def calc_distance(userLoc, bizLoc):
    return Distance(m=bizLoc.distance(userLoc) * locapi.DEG_TO_M)

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
        swp = Point(float(sw[1]), float(sw[0]))
        nep = Point(float(ne[1]), float(ne[0]))
        return (swp, nep)
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

class JoinedQuerySet(SearchQuerySet):
    def __init__(self, queries=[], *args, **kwargs):
        super(JoinedQuerySet, self).__init__(*args, **kwargs)
        self.queries = queries

    def _determine_backend(self):
        pass

    def __len__(self):
        if not self._result_count:
            self._result_count = 0
            for q in self.queries:
                self._result_count += q.query.get_count()
            if not self._result_count:
                self._result_count = 0
        return self._result_count - self._ignored_result_count

    def _fill_cache(self, start, end, **kwargs):
        results = []
        first = start
        total = 0
        page_size = end - start
        for q in self.queries:
            count = q.query.get_count()
            total += count
            cur_page_size = page_size
            if cur_page_size > count:
                cur_page_size = count
            q.query._reset()
            if first < total:
                print first, first + cur_page_size, page_size
                q.query.set_limits(first, first + cur_page_size)
                results += q.query.get_results(**kwargs)
                page_size -= cur_page_size
            first = max(first - cur_page_size, 0) 

        if results == None or len(results) == 0:
            return False

        if len(self._result_cache) == 0:
            self._result_cache = [None for i in range(total)]

        if start is None:
            start = 0

        if end is None:
            end = self.query.get_count()

        to_cache = self.post_process_results(results)
        self._result_cache[start:start + len(to_cache)] = to_cache
        return True

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
        self.admin = None
        self.sortPoint = DEF_POINT
        self.userPoint = DEF_POINT
        self.userCountry = DEF_COUNTRY
        self.ip_accurate = True
        # Start by IP Lookup to find point
        if ip:
            (point, country, accurate) = processGeoIp(ip)
            self.userCountry = country
            self.ip_accurate = accurate
            if point:
                self.sortPoint = point
                self.userPoint = point
        if not self.sortPoint:
            self.sortPoint = DEF_POINT
            self.userPoint = DEF_POINT
            self.userCountry = DEF_COUNTRY
        self.admin_level = 4
        if self.locationStr:
            self.filter_web_only = self.locationStr.lower() in WEB_ONLY_ARRAY
            self.filter_on_web = self.locationStr.lower() in WEB_LOC_ARRAY
            self.filter_current_location = self.locationStr.lower() in CUR_LOC_ARRAY
        else:
            self.filter_web_only = False
            self.filter_on_web = False
            self.filter_current_location = False
        if self.isOnWeb():
            pass
        if not self.isCurrentLocation() and not self.isOnWeb() and locationStr:
            res = locapi.googleBestMatch(locationStr, self.userPoint)
            if res:
                ref = res['reference']
                (centroid, bounding, admin) = locapi.googleDetailsToBounding(ref)
                self.admin = admin
                self.bounding = bounding
                if not self.boundingContains(self.sortPoint):
                    self.sortPoint = centroid
        if ll:
            self.ip_accurate = True
            geoloc = parseGeoLocation(ll)
            if geoloc:
                self.userPoint = geoloc;
                if not self.bounding or self.boundingContains(geoloc):
                    self.sortPoint = geoloc;

    def admin1(self):
        if self.admin and self.admin.has_key('administrative_area_level_1'):
            return locapi.admin1Map(self.admin['administrative_area_level_1']['short'])
        else:
            return None

    def country(self):
        if self.admin and self.admin.has_key('country'):
            return locapi.countryMap(self.admin['country']['short'])
        else:
            return None

    def myLocation(self):
        try:
            if self.admin and self.admin.has_key('country') \
                        and self.admin.has_key('administrative_area_level_1') \
                        and self.admin.has_key('administrative_area_level_2'):
                c = self.admin['country']['long']
                a1s, a1l = self.admin['administrative_area_level_1']['short'],\
                           self.admin['administrative_area_level_1']['long']
                try:
                    loc = self.admin['locality']['long']
                except:
                    loc = None
                if loc:
                    return "{0}, {1}, {2}".format(loc, a1s, c)
                else:
                    return "{0}, {1}, {2}".format(a1l, c)
        except:
            log.warn('error creating geolocation string')
        return None

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
        if self.bounding.distance(location) * locapi.DEG_TO_M <= locapi.DEF_RADIUS.m:
            return True
        return False


    def isWebOnly(self):
        return self.filter_web_only

    def isOnWeb(self):
        return self.filter_on_web

    def isCurrentLocation(self):
        return self.filter_current_location

class ApiProcess(object):
    def __init__(self, locationStr=None, ll=None, ip=None, lang=DEF_LANG):
        self.location = Location(locationStr=locationStr, ll=ll, ip=ip)
        self.lang = lang

    def userLocation(self):
        return self.location.userPoint

    def sortLocation(self):
        return self.location.sortPoint

    def isExactCategory(self, term):
        if term:
            return Category.objects.filter(name__iexact=term).exists()
        else:
            return False

    def exactMatch(self, term):
        s = u"exact_match_{}:{}".format(term, self.location.locationStr)
        if cache.get(s, True) == False:
            return (0, [])

        sqs = SearchQuerySet().models(Business)
        sqs = sqs.filter(name=term)
        sqs = sqs.filter(admin3_name=self.location.locationStr)
        sqs = sqs.filter(is_searchable=False)
        sqs = sqs.distance('location', self.sortLocation())

        m_len = len(sqs)
        if m_len == 1:
            cache.set(s, True, 60 * 60)
        else:
            cache.set(s, False, 60 * 60)
        return m_len, sqs

    def findFeatured(self):
        sqs = SearchQuerySet().models(Business)
        return sqs.filter(is_searchable=True, categories='Featured')

    def searchDirectory(self, term=None, since=None, geobounds=None,
                              radius=None, category=None, sort=None,
                              show_hidden=True, user=None):
        if show_hidden:
            (len_m, m) = self.exactMatch(term)
            if len_m == 1:
                return m

        featured = self.findFeatured()
        sqs = SearchQuerySet().models(Business)
        if user and user.id in LOCKED_USERS:
            sqs = sqs.filter(owner=user.id)
        sqs = sqs.filter(is_searchable=True)
        lang_cat=self.catDict(term)
        if term:
            formatted = wildcardFormat(term)
            sqs = sqs.filter(SQ(**lang_cat)
                           | SQ(name=term)
                           | SQ(name=formatted)
                           | SQ(description=term))
        if since:
            sqs = sqs.filter(published__gte=since)
        if category:
            sqs = self.querySetAddCategories(sqs, category)
        if self.location.isWebOnly():
            sqs = sqs.filter(SQ(has_online_business=True) & SQ(has_physical_business=False))
        elif self.location.isOnWeb():
            sqs = sqs.filter(SQ(has_online_business=True))
        if self.location.isOnWeb():
            if not term:
                sqs = sqs.order_by('-has_bitcoin_discount', '-score')
            else:
                sqs = sqs.order_by('-score')
        else:
            sqs = sqs.narrow('has_physical_business:true')
            if self.location.country():
                sqs = sqs.narrow(u'country:"{0}"'.format(self.location.country()));
                if self.location.admin1():
                    sqs = sqs.narrow(u'admin1_code:"{0}"'.format(self.location.admin1()))
            sqs = sqs.distance('location', self.sortLocation())
            if radius:
                sqs = sqs.dwithin('location', self.sortLocation(), D(m=radius))
            if geobounds:
                (sw, ne) = parseGeoBounds(geobounds)
                sqs = sqs.within('location', sw, ne)
            sqs = sqs.order_by('distance')
        return JoinedQuerySet(queries=[featured, sqs])

    def __filer_on_web__(self, sqs):
        inCountry = []
        outCountry = []
        for s in sqs:
            if s.country == self.location.userCountry:
                inCountry.append(s)
            else:
                outCountry.append(s)
        return inCountry + outCountry

    def __geolocation_filter__(self, sqs, geopoly, radius):
        newsqs = []
        if self.location.hasBounding:
            # Do we have a bounding box?
            for s in sqs:
                s.distance = s.distance
                s.bounded = False
                if s.location:
                    s.distance = Distance(m=s.location.distance(self.location.userPoint) * locapi.DEG_TO_M)
                    s.sortDistance = Distance(m=s.location.distance(self.location.sortPoint) * locapi.DEG_TO_M)
                    if self.location.boundingContains(s.location):
                        # Its within the bounding box
                        s.bounded = True
                        self.__append_if_within__(newsqs, s, poly=geopoly, radius=radius)
                    elif self.location.boundingExpandedContains(s.location):
                        # Outside of bounding, but within the DEF_RADIUS
                        self.__append_if_within__(newsqs, s, poly=geopoly, radius=radius)
            return newsqs
        else:
            for s in sqs:
                s.distance = s.distance
                s.bounded = False
                if s.location:
                    s.distance = Distance(m=s.location.distance(self.location.userPoint) * locapi.DEG_TO_M)
                    s.sortDistance = Distance(m=s.location.distance(self.location.sortPoint) * locapi.DEG_TO_M)
                    self.__append_if_within__(newsqs, s, poly=geopoly, radius=radius)
            return newsqs

    def __append_if_within__(self, ls, obj, poly=None, radius=None):
        if poly:
            if poly.contains(obj.location):
                ls.append(obj)
        elif radius:
            if obj.sortDistance.m < radius:
                ls.append(obj)
        else:
            ls.append(obj)

    def autocompleteBusiness(self, term=None, location=None, geolocation=None):
        if not term:
            return self.suggestNearCategories()

        sqs = SearchQuerySet()
        if location:
            fits = SQ(django_ct='directory.business') & SQ(is_searchable=True)
            if self.location.isWebOnly():
                fits = fits & SQ(has_online_business=True) & SQ(has_physical_business=False)
            elif self.location.isOnWeb():
                fits = fits & SQ(has_online_business=True)
        else:
            fits = SQ(django_ct='directory.business') & SQ(is_searchable=True)
        cats = SQ(django_ct='directory.category')
        if term:
            formatted = wildcardFormat(term)
            # place search
            fits = fits & SQ(content_auto=formatted)
            # category search
            if self.lang == DEF_LANG or not self.supportedLang():
                c = {'text': formatted}
            else:
                c = {self.lang + '_text': formatted}
            cats = cats & SQ(**c)
        sqs = sqs.filter(SQ(fits) | SQ(cats)).models(Business, Category)
        if self.location.isOnWeb() or self.location.isWebOnly():
            sqs = sqs.order_by('-has_bitcoin_discount')
        else:
            if self.location and self.location.bounding:
                sqs = self.boundSearchQuery(sqs, self.location)
        sqs = sqs[:10]
        return [autocompleteSerialize(result, self.lang) for result in sqs]

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
        if term:
            res = locapi.googleAutocomplete(term, self.sortLocation())
            return [r['description'] for r in res['predictions']]
        else:
            return []

    @staticmethod
    def isSupportedLang(lang):
        return lang in ('en', 'es')

    def supportedLang(self):
        return ApiProcess.isSupportedLang(self.lang)

    def catDict(self, term):
        if not self.supportedLang() or self.lang == DEF_LANG:
            lang_cat={'categories':term}
        else:
            lang_cat={self.lang + '_categories':term}
        return lang_cat

    def querySetAddCategories(self, sqs, category):
        f = None
        for cterm in category.split(","):
            d=self.catDict(cterm)
            q = SQ(**d)
            if not f:
                f = q
            else:
                f = f | q
        return sqs.filter(f)

    def suggestNearCategories(self):
        sqs = SearchQuerySet().models(Business)
        sqs = sqs.filter(is_searchable=True)
        if self.location.isWebOnly():
            sqs = sqs.filter(has_online_business=True, has_physical_business=False)
            sqs = sqs.order_by('-has_bitcoin_discount')
        elif self.location.isOnWeb():
            sqs = sqs.filter(has_online_business=True)
            sqs = sqs.order_by('-has_bitcoin_discount')
        else:
            sqs = sqs.filter(has_physical_business=True)
            sqs = sqs.distance('location', self.sortLocation())
            sqs = sqs.order_by('distance')

        if self.location and self.location.bounding:
            sqs = sqs[:25]
            sqs = self.boundSearchQuery(sqs, self.location)

        used = {}
        sqs = flatten([autocompleteSuggSerialize(s, used, self.lang) for s in sqs[:10]])
        return filter(lambda x : x is not None, sqs)

    def suggestNearText(self):
        if self.location.ip_accurate:
            point = self.sortLocation()
            nearText = nearTextFromPoint(point)
            if nearText:
                return nearText
        if self.location.ip:
            nearText = ipToLocationString(self.location.ip)
        if nearText:
            return nearText
        return DEF_LOC_STR

def getRequestIp(request):
    return request.META['REMOTE_ADDR']

def ipToLocationString(ip):
    (point, country, accurate) = processGeoIp(ip)
    if point and accurate:
        return nearTextFromPoint(point)
    if ALL_COUNTRY_LABELS.has_key(country):
        return ALL_COUNTRY_LABELS[country]
    else:
        return DEF_LOC_STR

def nearTextFromPoint(point):
    try:
        return locapi.googleNearby(point)
    except Exception as e:
        log.warn(e)
    return None

def processGeoIp(ip):
    if ip in ("10.0.2.2", "127.0.0.1"):
        ip = localToPublicIp()

    res = cache.get(ip, None)
    if res: res

    proc = subprocess.Popen(['geoiplookup', ip], stdout=subprocess.PIPE)
    data = proc.stdout.read()
    country = None
    for line in data.split('\n'):
        row = line.split(':')
        if len(row) == 2:
            point = None
            accuracy = True
            (k, v) = (row[0], row[1])
            if k.__contains__("Country"):
                country = processCountry(v)
            elif k.__contains__("City"):
                (point, accuracy) = processCity(v)
            if point:
                res = (point, country, accuracy)
                cache.set(ip, res, 60 * 60)
                return res
    res = (None, country, False)
    cache.set(ip, res, 60 * 60)
    return res

def localToPublicIp():
    """ This should only be called during development """
    res = cache.get('local_ip', None)
    if res:
        return res
    URL='http://www.networksecuritytoolkit.org/nst/tools/ip.php'
    try:
        import urllib
        ip = urllib.urlopen(URL).read().strip()
        cache.set('local_ip', ip)
        return ip
    except:
        log.warn('unable to look up ip')
    # Just return a default IP
    cache.set('local_ip', DEF_IP)
    return DEF_IP

def processCountry(row):
    try:
        v = row.strip().split(",")
        return v[0]
    except:
        return DEF_COUNTRY

def processCity(row):
    accuracy = True
    try:
        v = row.strip().split(",")
        if v[1].strip() == 'N/A':
            accuracy = False
        lat, lon = float(v[5]), float(v[6])
        return (Point(lon, lat), accuracy)
    except Exception as e:
        try:
            lat, lon = float(v[5]), float(v[6])
            return (Point(lon, lat), accuracy)
        except:
            log.warn(e)
    return (None, accuracy)

def sortedImages(biz_id):
    images = BusinessImage.objects.filter(business_id=biz_id)
    images = sorted([(i.isprimary, i) for i in images], key=lambda (i,j): i)
    images.reverse()
    return [i for _,i in images]


