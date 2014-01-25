from rest_framework import generics
from rest_framework.response import Response 
from rest_framework.views import APIView
import logging

from directory.models import Business, BusinessImage, Category
from restapi import api
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
    pk_url_kwarg = 'bizId'


class PhotosView(generics.ListAPIView):
    """ 
        Retrieve photos related to a business.
    """
    model = BusinessImage
    serializer_class = serializers.BusinessImageSerializer


class SearchView(generics.ListAPIView):
    """
        Comprehensive search of the businesses

        term --  term (optional)
        location -- (optional), 
        ll -- latitude,longitude (optional)
        radius -- radius (optional)
        bounds -- sw_latitude,sw_longitude|ne_latitude,ne_longitude (optional)
        category -- filter by category (optional))
        limit -- (optional)
        offset -- (optional)
        sort -- (optional) 0, default, best match. 1, sort based off distance
    """
    model = Business
    serializer_class = serializers.MiniBusinessSerializer

    def get_queryset(self):
        term = self.request.QUERY_PARAMS.get('term', None)
        location = self.request.QUERY_PARAMS.get('location', None)
        ll = self.request.QUERY_PARAMS.get('ll', None)
        radius = api.toInt(self.request, 'radius', api.RADIUS_DEFAULT)
        bounds = self.request.QUERY_PARAMS.get('bounds', None)
        category = self.request.QUERY_PARAMS.get('category', None)
        sort = api.toInt(self.request, 'sort', None)
        return api.searchDirectory(term=term, location=location, \
                                   geolocation=ll, geobounds=bounds, \
                                   radius=radius, category=category, sort=sort)


class AutoCompleteBusiness(generics.ListAPIView):
    """
        Autocomplete businesses
        term     -- Search term
        location -- Location string
        ll   -- Latitude,Longitude (optional)
    """
    model = Business
    serializer_class = serializers.AutoCompleteSerializer

    def get_queryset(self):
        term = self.request.QUERY_PARAMS.get('term', None)
        location = self.request.QUERY_PARAMS.get('location', None)
        ll = self.request.QUERY_PARAMS.get('ll', None)
        return api.autocompleteBusiness(term=term, location=location, geolocation=ll)


class AutoCompleteLocation(APIView):
    """
        Autocomplete location
        term -- Search term
        ll   -- Latitude,Longitude (optional)
    """
    model = Business

    def get(self, request, *args, **kwargs):
        term = self.request.QUERY_PARAMS.get('term', None)
        ll = self.request.QUERY_PARAMS.get('ll', None)
        results = api.autocompleteLocation(term=term, geolocation=ll)
        return Response({ 'results':  results })


class LocationSuggest(APIView):
    """
        Suggests a default location based on the IP address and lat/lon.
        ll -- Latitude,Longitude (optional)

        If lat/lon aren't provided, then this method falls back to using the IP
        address.
    """
    model = Business

    def get(self, request, *args, **kwargs):
        ll = self.request.QUERY_PARAMS.get('ll', None)
        ip = request.META['REMOTE_ADDR']
        results = api.suggestNearText(ip=ip, geolocation=ll)
        return Response({ 'near':  results })

