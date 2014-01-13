from django.contrib.gis.geos import Point
from rest_framework import generics
from rest_framework.response import Response 
from rest_framework.views import APIView
import logging
import subprocess

from directory.models import Business, BusinessImage, Category
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
    """
    model = Business
    serializer_class = serializers.AutoCompleteSerializer

    def get_queryset(self):
        q = self.request.QUERY_PARAMS.get('q', None)
        lat = self.request.QUERY_PARAMS.get('lat', None)
        lon = self.request.QUERY_PARAMS.get('lon', None)
        if q:
            qs = Business.objects.filter(name__icontains=q)
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
        # lat = self.request.QUERY_PARAMS.get('lat', None)
        # lon = self.request.QUERY_PARAMS.get('lon', None)
        ip = request.META['REMOTE_ADDR']
        if ip in ("10.0.2.2", "127.0.0.1"):
            ip = "24.152.191.12" 
        results = process_geoip(ip)
        return Response(results)

def process_geoip(ip):
    proc = subprocess.Popen(['geoiplookup', ip], stdout=subprocess.PIPE)
    data = proc.stdout.read()
    results = []
    for line in data.split('\n'):
        row = line.split(':')
        if len(row) == 2:
            data = None
            (k, v) = (row[0], row[1])
            if k.__contains__("City"):
                data = process_geocity(v)
            if data:
                results += [data]
    return results

def process_geocountry(row):
    return {
        'country': row
    }

def process_geocity(row):
    try:
        v = row.strip().split(",")
        return {
            'country': v[0].strip(),
            'state_abbrev': v[1].strip(),
            'city': v[2].strip(),
            'postal': v[3].strip(),
            'lat': v[4].strip(),
            'lon': v[5].strip()
        }
    except:
        log.warn('Problem parsing city')
    return None

