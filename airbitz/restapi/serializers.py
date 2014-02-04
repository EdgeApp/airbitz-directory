from rest_framework import serializers
from rest_framework import fields
from rest_framework import pagination

from directory.models import Business, BusinessHours, \
                             BusinessImage, Category, \
                             SocialId
from location.models import GeoNameZip

class PointField(fields.Field):
    type_name = 'PointField'

    def field_to_native(self, obj, field_name):
        return {'latitude': obj.center.y, 'longitude': obj.center.x}

class BoundingBoxField(fields.Field):
    type_name = 'BoundingBoxField'

    def field_to_native(self, obj, field_name):
        return {'x': 0.0, 'y': 0.0, 'height': 0.25, 'width': 1.0}

class BusinessHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessHours
        fields = ('dayOfWeek','hourStart', 'hourEnd', )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name','description')

class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialId
        fields = ('social_type', 'social_id', 'social_url')

class MiniBusinessSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(source='categories')
    social = SocialSerializer(source='socialid_set')
    state = serializers.CharField(source='admin1_code')
    county = serializers.CharField(source='admin2_name')
    city = serializers.CharField(source='admin3_name')
    has_bitcoin_discount = serializers.CharField(source='has_bitcoin_discount')
    center = PointField()

    class Meta:
        model = Business
        fields = ('name',
                  'categories',
                  'social',
                  'description',
                  'website',
                  'phone',
                  'city',
                  'county',
                  'state', 
                  'postalcode',
                  'country',
                  'center', )

class PaginatedMiniBizSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = MiniBusinessSerializer

class BusinessSerializer(serializers.ModelSerializer):
    state = serializers.CharField(source='admin1_code')
    county = serializers.CharField(source='admin2_name')
    city = serializers.CharField(source='admin3_name')
    hours = BusinessHoursSerializer(source='businesshours_set')
    categories = CategorySerializer(source='categories')
    social = SocialSerializer(source='socialid_set')
    center = PointField()

    class Meta:
        model = Business
        fields = ('name',
                  'categories',
                  'social',
                  'description',
                  'website',
                  'phone',
                  'city',
                  'county',
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
    bounding_box = BoundingBoxField()

    class Meta:
        model = BusinessImage
        fields = ('image', 'height', 'width', 'bounding_box',)

class AutoCompleteSerializer(serializers.Serializer):
    pk = serializers.Field()
    name = serializers.CharField(required=False, max_length=100)

class AutoCompleteLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoNameZip
        fields = ('admin_name2',
                  'admin_code1',
                 )

