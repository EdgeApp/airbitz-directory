from rest_framework import serializers
from rest_framework import fields
from django.contrib.gis.geos import GEOSGeometry, GEOSException
from django.contrib.gis.gdal import OGRException
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import json

from directory.models import Business, BusinessHours, \
                             BusinessImage, Category, \
                             GeoNameZip

class PointField(fields.WritableField):
    type_name = 'PointField'

    def to_native(self, value):
        if isinstance(value, dict) or value is None:
            return value
        return json.loads(value.geojson)

    def from_native(self, value):
        if value == '' or value is None:
            return value

        if isinstance(value, dict):
            value = json.dumps(value)

        try:
            return GEOSGeometry(value)
        except (ValueError, GEOSException, OGRException, TypeError):
            raise ValidationError(_('Invalid format: string or unicode input unrecognized as WKT EWKT, and HEXEWKB.'))

        return value


class BusinessHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessHours
        fields = ('dayOfWeek','hourStart', 'hourEnd', )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name','description')

class MiniBusinessSerializer(serializers.ModelSerializer):
    category = CategorySerializer(source='category')
    center = PointField()

    class Meta:
        model = Business
        fields = ('name',
                  'category',
                  'description',
                  'city',
                  'state', 
                  'postalcode',
                  'country',
                  'center', )

class BusinessSerializer(serializers.ModelSerializer):
    hours = BusinessHoursSerializer(source='businesshours_set')
    category = CategorySerializer(source='category')
    center = PointField()

    class Meta:
        model = Business
        fields = ('name',
                  'category',
                  'description',
                  'city',
                  'state', 
                  'postalcode',
                  'country',
                  'center',
                  'hours',
                  'has_physical_business', 
                  'has_online_business',
                  'has_bitcoin_discount', )

class BusinessImageSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = BusinessImage
        fields = ('image', 'height', 'width')

class AutoCompleteSerializer(serializers.Serializer):
    pk = serializers.Field()
    name = serializers.CharField(required=False, max_length=100)

class AutoCompleteLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoNameZip
        fields = ('admin_name2',
                  'admin_code1',
                 )

