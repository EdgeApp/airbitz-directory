from django.contrib.auth.models import User
from django.contrib.gis.measure import Distance
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from haystack.query import SearchQuerySet
from rest_framework import authentication as auth
from rest_framework import exceptions
from rest_framework import generics, filters
from rest_framework import permissions as perm
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework_throttling.throttling import PerUserThrottle

import logging

from directory.models import Business, BusinessImage, Category
from restapi import api
from restapi import locapi
from restapi import serializers 
from restapi import tasks

log=logging.getLogger("airbitz." + __name__)

DEFAULT_PAGE_SIZE=20

class DemoAuthentication(auth.BaseAuthentication):
    def authenticate(self, request):
        try:
            user = User.objects.get(username='demodan')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        return (user, None)

class BetterTokenAuthentication(auth.TokenAuthentication):
    def authenticate(self, request):
        if request.QUERY_PARAMS.has_key('api_key'):
            token = request.QUERY_PARAMS.get('api_key')
            return self.authenticate_credentials(token)

        a = auth.get_authorization_header(request).split()
        if not a or a[0].lower() != b'token':
            return None

        if len(a) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(a) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(a[1])

PERMS=(BetterTokenAuthentication, auth.SessionAuthentication,)
AUTH=(perm.IsAuthenticated, )

class InternalOrderFilter(filters.OrderingFilter):
    ordering_param = 'sort'

class CategoryView(generics.ListAPIView):
    """
        Retrieve business categories. 

        sort -- which field sort by, either 'name' or 'level'
        api_key -- API Key
    """
    model = Category
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()
    pagination_serializer_class = serializers.LastUpdatedSerializer
    filter_backends = (InternalOrderFilter,)
    ordering_fields = ('name', 'level')
    authentication_classes = PERMS
    permission_classes = AUTH
    max_paginate_by = 500
    paginate_by = 500
    throttle_classes = (PerUserThrottle, )

    def get_queryset(self):
        tasks.ga_send(self.request, 'api::CategoryView');
        return super(CategoryView, self).get_queryset()

class BusinessView(generics.RetrieveAPIView):
    """
        Retrieve detailed information about a business.

        ll -- latitude,longitude
        api_key -- API Key
    """
    serializer_class = serializers.BusinessSerializer
    lookup_url_kwarg = 'bizId'
    authentication_classes = PERMS
    permission_classes = AUTH
    throttle_classes = (PerUserThrottle, )

    def get_queryset(self):
        tasks.ga_send(self.request, 'api::BusinessView');

        bizId = self.kwargs['bizId']
        sqs = SearchQuerySet().models(Business).filter(django_id=bizId)

        ll = self.request.QUERY_PARAMS.get('ll', None)
        if ll:
            try:
                point = api.parseGeoLocation(ll)
                sqs = sqs.distance('location', point)
            except:
                log.warn('unable to parse geolocation')
        return sqs

    def retrieve(self, request, *args, **kwargs):
        """
        Rather than use GeoDjago distance() function we calculate it manaully
        because it uses st_distance_sphere/st_distance_spheriod instead of
        st_distance. Classic!
        """
        try:
            self.object = self.get_queryset()[0]
        except:
            raise Http404
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)

class PhotosView(generics.ListAPIView):
    """ 
        Retrieve photos related to a business.

        api_key -- API Key
    """
    model = BusinessImage
    serializer_class = serializers.BusinessImageSerializer
    authentication_classes = PERMS
    permission_classes = AUTH
    throttle_classes = (PerUserThrottle, )

    def get_queryset(self):
        bizId = int(self.kwargs['bizId'])
        return api.sortedImages(bizId)


class SearchView(generics.ListAPIView):
    """
        Comprehensive search of the businesses

        term --  The term to search against, currently only searchs business names 
        location -- location string such as "San Diego, CA" , 
        ll -- latitude,longitude 
        radius -- search radius in meters 
        bounds -- bounding box of search area. sw_latitude,sw_longitude|ne_latitude,ne_longitude 
        category -- filter by category, can be a comma delimited string such as "Health,Finance" 
        since -- Only show businesses published since the given datetime
        page_size -- How many businesses each page, defaults to 20, max of 50 
        page -- Which page of data to return 
        sort --  0: default, best match. 1: sort based off distance
        api_key -- API Key
    """
    serializer_class = serializers.MiniBusinessSerializer
    paginate_by = DEFAULT_PAGE_SIZE
    paginate_by_param = 'page_size'
    max_paginate_by = 50
    authentication_classes = PERMS
    permission_classes = AUTH
    throttle_classes = (PerUserThrottle, )

    def get_queryset(self):
        ser = serializers.SearchSerializer(data=self.request.GET)
        if not ser.is_valid():
            return []

        obj=ser.object

        # Notify google analytics
        tasks.ga_send(self.request, 'api::search');

        a = api.ApiProcess(locationStr=obj.location, ll=obj.ll)
        return a.searchDirectory(term=obj.term, geobounds=obj.bounds, since=obj.since, \
                                 radius=obj.radius, category=obj.category, sort=obj.sort)



class AutoCompleteBusiness(APIView):
    """
        Autocompletes base on business name.

        term     -- The term to autocomplete
        location -- Location string such as "San Diego, CA"
        ll   -- Latitude,Longitude 
        api_key -- API Key
    """
    authentication_classes = PERMS
    permission_classes = AUTH
    model = Business
    throttle_classes = (PerUserThrottle, )

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
        api_key -- API Key
    """
    authentication_classes = PERMS
    permission_classes = AUTH
    model = Business
    throttle_classes = (PerUserThrottle, )

    def get(self, request, *args, **kwargs):
        term = self.request.QUERY_PARAMS.get('term', None)
        ll = self.request.QUERY_PARAMS.get('ll', None)
        ip = api.getRequestIp(request)
        a = api.ApiProcess(ll=ll, ip=ip)
        results = a.autocompleteLocation(term=term)
        if results:
            results = results[:DEFAULT_PAGE_SIZE]
        return Response({ 'results':  results })


class CategorySuggest(APIView):
    """
        Suggests a default category listing
        ll -- Latitude,Longitude 
        api_key -- API Key

        If lat/lon aren't provided, then this method falls back to using the IP
        address.
    """
    authentication_classes = PERMS
    permission_classes = AUTH
    model = Business
    throttle_classes = (PerUserThrottle, )

    def get(self, request, *args, **kwars):
        location = self.request.QUERY_PARAMS.get('location', None)
        ll = self.request.QUERY_PARAMS.get('ll', None)
        a = api.ApiProcess(locationStr=location, ll=ll)
        results = a.suggestNearCategories()[:DEFAULT_PAGE_SIZE]
        return Response({ 'results':  results })


class LocationSuggest(APIView):
    """
        Suggests a default location based on the IP address and lat/lon.
        ll -- Latitude,Longitude 
        api_key -- API Key

        If lat/lon aren't provided, then this method falls back to using the IP
        address.
    """
    authentication_classes = PERMS
    permission_classes = AUTH
    model = Business
    throttle_classes = (PerUserThrottle, )

    def get(self, request, *args, **kwargs):
        ll = self.request.QUERY_PARAMS.get('ll', None)
        ip = api.getRequestIp(request)
        a = api.ApiProcess(ll=ll, ip=ip)
        results = a.suggestNearText()
        return Response({ 'near':  results })


def page_api_v1_documentation(request):

    context = {
        'page_title': 'Airbitz Directory API v1',
        'page_description': 'Documentation for use of the Airbitz directory api version 1.',
    }
    return render_to_response('pages/page_api_v1_documentation.html', RequestContext(request, context))
