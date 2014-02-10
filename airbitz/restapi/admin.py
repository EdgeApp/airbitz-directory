from django.contrib.gis.geos import Point
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework import pagination
from rest_framework import serializers
from rest_framework import fields
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser

import logging

from directory.models import Business, Category
from restapi.api import querySetAddLocation

log=logging.getLogger("airbitz." + __name__)

DEFAULT_PAGE_SIZE=20

class EchoField(fields.Field):
    type_name = 'EchoField'

    def field_to_native(self, obj, field_name):
        request = self.context.get('request')
        return request.QUERY_PARAMS.get('sEcho', '1')

class DataTablePagination(pagination.BasePaginationSerializer):
    iTotalRecords = serializers.Field(source='paginator.count')
    iTotalDisplayRecords = serializers.Field(source='paginator.count')
    sEcho = EchoField();
    results_field = 'aaData'


class AdminPointField(serializers.WritableField):
    type_name = 'AdminPointField'

    def to_native(self, obj):
        return {'latitude': obj.y, 'longitude': obj.x}

    def from_native(self, data):
        return Point((data['longitude'], data['latitude']))

class AdminCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', )

class AdminBizSerializer(serializers.ModelSerializer):
    categories = AdminCategorySerializer(source='categories', many=True, read_only=False)
    center = AdminPointField(source='center')
    class Meta:
        model = Business

class AdminCategory(ListCreateAPIView):
    serializer_class = AdminCategorySerializer
    filter_fields = ('name', )
    permission_classes = (IsAdminUser,)
    model = Category

class AdminCategoryDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = AdminCategorySerializer
    permission_classes = (IsAdminUser,)
    model = Category

class DataTablePaginate(Paginator):

    converted = False

    def validate_number(self, page):
        """ Data Tables supplies the row, not page number """
        if self.converted:
            return page
        else:
            try:
                number = (int(page) / self.per_page) + 1
                self.converted = True
            except (TypeError, ValueError):
                pass
            print page, self.per_page, number
            return number

class AdminBusinessView(ListCreateAPIView):
    serializer_class = AdminBizSerializer
    permission_classes = (IsAdminUser,)
    model = Business
    paginate_by_param = 'iDisplayLength'
    page_kwarg = 'iDisplayStart'
    pagination_serializer_class = DataTablePagination
    paginator_class = DataTablePaginate
    allow_empty = True

    def paramArray(self, name, request):
        l = []
        i = 0
        while request.QUERY_PARAMS.get(name + str(i), None):
            l.append(request.QUERY_PARAMS.get(name + str(i)))
            i = i + 1
        return l

    def formatDir(self, c, d):
        if d == "desc":
            return '-' + c
        else:
            return c

    def get_queryset(self):
        search = self.request.QUERY_PARAMS.get('sSearch', None)
        location = self.request.QUERY_PARAMS.get('location', None)
        cols = self.paramArray('mDataProp_', self.request)
        sorts = self.paramArray('iSortCol_', self.request)
        dirs = self.paramArray('sSortDir_', self.request)

        q = Business.objects.all()
        if search:
            q = q.filter(Q(name__icontains=search)
                       | Q(categories__name__icontains=search))
        if location:
            (q, _) = querySetAddLocation(q, location)
        if sorts:
            l = []
            for (s, d) in zip(sorts, dirs):
                c = cols[int(s)]
                l.append(self.formatDir(c, d))
            q = q.order_by(*l)
        print q.query
        return q

class AdminBusinessDetails(RetrieveUpdateDestroyAPIView):
    serializer_class = AdminBizSerializer
    permission_classes = (IsAdminUser,)
    model = Business

