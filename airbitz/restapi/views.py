from django.contrib.gis.geos import Point
from rest_framework import generics
from rest_framework.response import Response 
from rest_framework.views import APIView
import logging
import subprocess

from directory.models import Business, BusinessImage, Category, GeoName
from restapi import serializers 

log=logging.getLogger("airbitz." + __name__)

class CategoryView(generics.ListAPIView):
    """
        Retrieve business categories. 
    """
    model = Category
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()

class BusinessView(generics.RetrieveAPIView):
    """
        Retrieve detailed information about a business.
    """
    serializer_class = serializers.BusinessSerializer
    model = Business
    def get(self, request, bizId):
        return Response(Business.objects.get(pk=bizId))

class PhotosView(generics.ListAPIView):
    """ 
        Retrieve photos related to a business.
    """
    model = BusinessImage
    serializer_class = serializers.BusinessImageSerializer
    def get(self, request, bizId):
        return Response(BusinessImage.objects.filter(business_id=bizId))

class SearchView(generics.ListAPIView):
    """
        Comprehensive search of the businesses
        q -- The search term (optional)
        lat -- Latitude (optional)
        lng -- Latitude (optional)
    """
    model = Business
    serializer_class = serializers.MiniBusinessSerializer

    def get_queryset(self):
        q = self.request.QUERY_PARAMS.get('q', None)
        if q:
            return Business.objects.filter(name__icontains=q)
        else:
            return Business.objects.none()

class AutoCompleteBusiness(generics.ListAPIView):
    """
        Autocomplete businesses
    """
    model = Business
    serializer_class = serializers.AutoCompleteSerializer

    def get_queryset(self):
        q = self.request.QUERY_PARAMS.get('q', None)
        near = self.request.QUERY_PARAMS.__contains__('near')
        lat = self.request.QUERY_PARAMS.get('lat', None)
        lon = self.request.QUERY_PARAMS.get('lon', None)
        if q:
            if near:
                qs = Business.objects.filter(city__icontains=q)
            else:
                qs = Business.objects.filter(name__icontains=q)
            if lat and lon:
                origin = Point((float(lon), float(lat)))
                qs = qs.distance(origin).order_by('distance')
            return qs
        else:
            return Business.objects.none()


class AutoCompleteLocation(generics.ListAPIView):
    """
        Autocomplete location
        q   -- Query
        lon -- Longitude (optional)
        lat -- Latitude (optional)
    """
    model = GeoName
    serializer_class = serializers.AutoCompleteLocationSerializer

    def get_queryset(self):
        q = self.request.QUERY_PARAMS.get('q', None)
        lat = self.request.QUERY_PARAMS.get('lat', None)
        lon = self.request.QUERY_PARAMS.get('lon', None)
        if q:
            qs = GeoName.objects.filter(place_name__icontains=q)
            if lat and lon:
                origin = Point((float(lon), float(lat)))
                qs = qs.distance(origin).order_by('distance')
            return qs
        else:
            return Business.objects.none()


class CitySuggest(APIView):
    """
        Suggests a default city based on the IP address and lat/lon.
        lat -- Latitude (optional)
        lon -- Longitude (optional)

        If lat/lon aren't provided, then this method falls back to using the IP
        address.
    """
    model = Business
    serializer_class = serializers.CitySuggestSerializer

    def get(self, request, *args, **kwargs):
        lat = self.request.QUERY_PARAMS.get('lat', None)
        lon = self.request.QUERY_PARAMS.get('lon', None)
        ip = request.META['REMOTE_ADDR']
        results = buildNearText(ip, lat, lon)
        return Response({ 'near':  results })

def buildNearText(ip, lat=None, lon=None):
    if lat and lon:
        results = process_geoip(ip)
    else:
        results = process_geoip(ip)
    return results

def process_geoip(ip):
    if ip in ("10.0.2.2", "127.0.0.1"):
        ip = local_to_public_ip()
    proc = subprocess.Popen(['geoiplookup', ip], stdout=subprocess.PIPE)
    data = proc.stdout.read()
    for line in data.split('\n'):
        row = line.split(':')
        if len(row) == 2:
            data = None
            (k, v) = (row[0], row[1])
            if k.__contains__("City"):
                data = process_geocity(v)
            if data:
                return data
    return None

def local_to_public_ip():
    """ This should only be called during development """
    URL='http://www.networksecuritytoolkit.org/nst/tools/ip.php'
    try:
        import urllib
        return urllib.urlopen(URL).read().strip()
    except:
        log.warn('unable to look up ip')
    # Just return a default IP
    return '24.152.191.12'
    

def process_geocountry(row):
    return row

def process_geocity(row):
    try:
        v = row.strip().split(",")
        return "{0}, {1}".format(v[2].strip(), v[1].strip())
    except Exception as e:
        log.warn(e)
    return None

