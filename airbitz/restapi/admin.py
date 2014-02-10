from django.contrib.gis.geos import Point
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import ValidationError
from rest_framework import fields
from rest_framework import pagination
from rest_framework import serializers
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

import logging

from directory.models import Business, BusinessHours, Category, SocialId
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

class AdminSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialId
        fields = ('social_type', 'social_id', 'social_url')

class AdminHoursSerializer(serializers.ModelSerializer):
    hourStart = fields.CharField(required=False);
    hourEnd = fields.CharField(required=False);
    class Meta:
        model = BusinessHours
        fields = ('id', 'dayOfWeek','hourStart', 'hourEnd', )

class AdminBizSerializer(serializers.ModelSerializer):
    categories = AdminCategorySerializer(source='categories', many=True)
    hours = AdminHoursSerializer(source='businesshours_set', many=True)
    center = AdminPointField(source='center')

    class Meta:
        model = Business

class AdminCategory(ListCreateAPIView):
    serializer_class = AdminCategorySerializer
    filter_fields = ('name', )
    permission_classes = (IsAdminUser,)
    model = Category
    paginate_by = 1000

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

    def __update_cats__(self, request):
        if request.DATA.has_key('categories'):
            cats = self.object.categories.all()
            delcats = dict((c.id, c) for c in cats)
            for c in request.DATA['categories']:
                if not c.has_key('name') or not c.has_key('id'):
                    continue
                if c['id'] == 0:
                    newcat, _ = Category.objects.get_or_create(name=c['name'])
                    c['id'] = newcat.id
                    self.object.categories.add(newcat)
                elif not any([c['id'] == c2.id for c2 in cats]):
                    self.object.categories.add(Category.objects.get(id=c['id']))

                if delcats.has_key(c['id']):
                    delcats.pop(c['id'])
            for i in delcats.itervalues():
                self.object.categories.remove(i)

            catList = []
            self.object = Business.objects.get(id=self.object.id)
            for c in self.object.categories.all():
                serial = AdminCategorySerializer(c)
                catList.append(serial.data)
            request.DATA['categories'] = catList

    def __update_hours__(self, request):
        if request.DATA.has_key('hours'):
            hours = self.object.businesshours_set.all()
            delhours = dict((c.id, c) for c in hours)
            print delhours
            for c in request.DATA['hours']:
                print c
                if not c.has_key('id'):
                    continue
                if c['id'] == 0:
                    newhour = BusinessHours.objects.create(business=self.object,\
                                                           dayOfWeek=c['dayOfWeek'],\
                                                           hourStart=c['hourStart'],\
                                                           hourEnd=c['hourEnd'])
                    c['id'] = newhour.id
                if delhours.has_key(c['id']):
                    d = delhours[c['id']]
                    d.dayOfWeek = c['dayOfWeek']
                    d.hourStart = c['hourStart']
                    d.hourEnd = c['hourEnd']
                    d.save()
                    delhours.pop(c['id'])
            for i in delhours.itervalues():
                print 'deleting ', i
                i.delete()

            hourList = []
            self.object = Business.objects.get(id=self.object.id)
            for h in self.object.businesshours_set.all():
                serial = AdminHoursSerializer(h)
                hourList.append(serial.data)
            request.DATA['hours'] = hourList

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        self.object = self.get_object_or_none()

        if self.object is None:
            created = True
            save_kwargs = {'force_insert': True}
            success_status_code = status.HTTP_201_CREATED
        else:
            created = False
            save_kwargs = {'force_update': True}
            success_status_code = status.HTTP_200_OK

        serializer = self.get_serializer(self.object, data=request.DATA,
                                         files=request.FILES, partial=partial)


        self.__update_cats__(request)
        self.__update_hours__(request)
        if serializer.is_valid():
            try:
                self.pre_save(serializer.object)
            except ValidationError as err:
                return Response(err.message_dict, status=status.HTTP_400_BAD_REQUEST)
            self.object = serializer.save(**save_kwargs)
            self.post_save(self.object, created=created)
            return Response(serializer.data, status=success_status_code)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

