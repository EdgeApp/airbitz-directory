from django.contrib.gis.geos import Point
from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser

import logging

from directory.models import Business, Category

log=logging.getLogger("airbitz." + __name__)

DEFAULT_PAGE_SIZE=20

class AdminPointField(serializers.WritableField):
    type_name = 'AdminPointField'

    def to_native(self, obj):
        print obj
        return {'latitude': obj.y, 'longitude': obj.x}

    def from_native(self, data):
        print data
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

class AdminBusinessView(ListCreateAPIView):
    serializer_class = AdminBizSerializer
    permission_classes = (IsAdminUser,)
    model = Business

class AdminBusinessDetails(RetrieveUpdateDestroyAPIView):
    serializer_class = AdminBizSerializer
    permission_classes = (IsAdminUser,)
    model = Business


