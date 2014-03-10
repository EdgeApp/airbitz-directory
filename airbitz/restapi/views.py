from django.contrib.auth.models import User
from rest_framework import authentication as auth
from rest_framework import permissions as perm
from rest_framework import exceptions
from rest_framework import generics, filters
from rest_framework.response import Response 
from rest_framework.views import APIView

import logging

from directory.models import Business, BusinessImage, Category
from restapi import api
from restapi import serializers 

log=logging.getLogger("airbitz." + __name__)

DEFAULT_PAGE_SIZE=20

class DemoAuthentication(auth.BaseAuthentication):
    def authenticate(self, request):
        try:
            user = User.objects.get(username='demodan')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        return (user, None)

PERMS=(DemoAuthentication, auth.TokenAuthentication, auth.SessionAuthentication,)
AUTH=(perm.IsAuthenticated, )

class InternalOrderFilter(filters.OrderingFilter):
    ordering_param = 'sort'

class CategoryView(generics.ListAPIView):
    """
        Retrieve business categories. 

        sort -- which field sort by, either 'name' or 'level'
    """
    model = Category
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()
    pagination_serializer_class = serializers.LastUpdatedSerializer
    filter_backends = (InternalOrderFilter,)
    ordering_fields = ('name', 'level')
    authentication_classes = PERMS
    permission_classes = AUTH

class BusinessView(generics.RetrieveAPIView):
    """
        Retrieve detailed information about a business.
    """
    serializer_class = serializers.BusinessSerializer
    queryset = Business.objects.filter(status='PUB')
    pk_url_kwarg = 'bizId'
    authentication_classes = PERMS
    permission_classes = AUTH


class PhotosView(generics.ListAPIView):
    """ 
        Retrieve photos related to a business.
    """
    model = BusinessImage
    serializer_class = serializers.BusinessImageSerializer
    authentication_classes = PERMS
    permission_classes = AUTH


class SearchView(generics.ListAPIView):
    """
        Comprehensive search of the businesses

        term --  The term to search against, currently only searchs business names 
        location -- location string such as "San Diego, CA" , 
        ll -- latitude,longitude 
        radius -- search radius in meters 
        bounds -- bounding box of search area. sw_latitude,sw_longitude|ne_latitude,ne_longitude 
        category -- filter by category, can be a comma delimited string such as "Health,Finance" 
        page_size -- How many businesses each page, defaults to 20, max of 50 
        page -- Which page of data to return 
        sort --  0: default, best match. 1: sort based off distance
    """
    queryset = Business.objects.all()
    serializer_class = serializers.MiniBusinessSerializer
    paginate_by = DEFAULT_PAGE_SIZE
    paginate_by_param = 'page_size'
    max_paginate_by = 50
    authentication_classes = PERMS
    permission_classes = AUTH

    def get_queryset(self):
        term = self.request.QUERY_PARAMS.get('term', None)
        location = self.request.QUERY_PARAMS.get('location', None)
        ll = self.request.QUERY_PARAMS.get('ll', None)
        radius = api.toInt(self.request, 'radius', None)
        bounds = self.request.QUERY_PARAMS.get('bounds', None)
        category = self.request.QUERY_PARAMS.get('category', None)
        sort = api.toInt(self.request, 'sort', None)

        a = api.ApiProcess(locationStr=location, ll=ll)
        return a.searchDirectory(term=term, geobounds=bounds, \
                                   radius=radius, category=category, sort=sort)


class AutoCompleteBusiness(APIView):
    """
        Autocompletes base on business name.

        term     -- The term to autocomplete
        location -- Location string such as "San Diego, CA"
        ll   -- Latitude,Longitude 
    """
    authentication_classes = PERMS
    permission_classes = AUTH
    model = Business

    def get(self, request, *args, **kwars):
        term = self.request.QUERY_PARAMS.get('term', None)
        location = self.request.QUERY_PARAMS.get('location', None)
        ll = self.request.QUERY_PARAMS.get('ll', None)
        a = api.ApiProcess(locationStr=location, ll=ll)
        results = a.autocompleteBusiness(term=term)[:DEFAULT_PAGE_SIZE]
        return Response({ 'results':  results })


class AutoCompleteLocation(APIView):
    """
        Autocomplete location.

        term -- The location string to autocomplete
        ll   -- Latitude,Longitude 
    """
    authentication_classes = PERMS
    permission_classes = AUTH
    model = Business

    def get(self, request, *args, **kwargs):
        term = self.request.QUERY_PARAMS.get('term', None)
        ll = self.request.QUERY_PARAMS.get('ll', None)
        ip = api.getRequestIp(request)
        a = api.ApiProcess(ll=ll, ip=ip)
        results = a.autocompleteLocation(term=term)[:DEFAULT_PAGE_SIZE]
        return Response({ 'results':  results })


class LocationSuggest(APIView):
    """
        Suggests a default location based on the IP address and lat/lon.
        ll -- Latitude,Longitude 

        If lat/lon aren't provided, then this method falls back to using the IP
        address.
    """
    authentication_classes = PERMS
    permission_classes = AUTH
    model = Business

    def get(self, request, *args, **kwargs):
        ll = self.request.QUERY_PARAMS.get('ll', None)
        ip = api.getRequestIp(request)
        a = api.ApiProcess(ll=ll, ip=ip)
        results = a.suggestNearText()[:DEFAULT_PAGE_SIZE]
        return Response({ 'near':  results })

