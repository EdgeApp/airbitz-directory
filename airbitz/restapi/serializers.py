from django.db.models import Max
from rest_framework import fields
from rest_framework import pagination
from rest_framework import serializers
from django.contrib.gis.measure import Distance

from directory.models import Business, BusinessImage, Category
from location.models import GeoNameZip

from restapi import locapi
from restapi.api import parseGeoLocation

import json

class ImageTagsField(serializers.Field):
    def field_to_native(self, obj, field_name):
        return [t.name for t in obj.tags.all()]

class MobileUrl(serializers.Field):
    def field_to_native(self, obj, field_name):
        return obj.mobile_photo.url

class MobileHeight(serializers.Field):
    def field_to_native(self, obj, field_name):
        return obj.mobile_photo.height

class MobileWidth(serializers.Field):
    def field_to_native(self, obj, field_name):
        return obj.mobile_photo.width

class MobileThumbnail(serializers.Field):
    def field_to_native(self, obj, field_name):
        return obj.mobile_thumbnail.url

class LastUpdated(serializers.Field):
    def field_to_native(self, obj, field_name):
        m = Category.objects.all().aggregate(Max('modified'))
        return m['modified__max']

class DistanceField(serializers.Field):
    def field_to_native(self, obj, field_name):
        if hasattr(obj, 'distance') and obj.distance:
            return obj.distance.m
        else:
            return None

class LastUpdatedSerializer(pagination.PaginationSerializer):
    last_updated = LastUpdated(source='*')

class PointField(fields.Field):
    type_name = 'PointField'

    def field_to_native(self, obj, field_name):
        if obj.location:
            return {'latitude': obj.location.y, 'longitude': obj.location.x}
        else:
            return None

class BoundingBoxField(fields.Field):
    type_name = 'BoundingBoxField'

    def field_to_native(self, obj, field_name):
        return {'x': 0.0, 'y': 0.0, 'height': 0.25, 'width': 1.0}

class BusinessImageSerializer(serializers.ModelSerializer):
    image = MobileUrl(source='*')
    height = MobileHeight(source='*')
    width = MobileWidth(source='*')
    thumbnail = MobileThumbnail(source='*')
    bounding_box = BoundingBoxField()
    tags = ImageTagsField(source='*')

    class Meta:
        model = BusinessImage
        fields = ('image', 'height', 'width', 'thumbnail', 'bounding_box', 'tags', )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'level', )

class JsonSerializer(serializers.Field):
    def __init__(self, islist=False, *args, **kwargs):
        self.islist = islist
        super(JsonSerializer, self).__init__(*args, **kwargs)

    def field_to_native(self, obj, field_name):
        val = get_component(obj, self.source) or ''
        if val:
            return json.loads(val)
        elif self.islist:
            return []
        else:
            return {}

class CharSerializer(serializers.Field):
    def field_to_native(self, obj, field_name):
        return get_component(obj, self.source) or ''

class PhoneSerializer(serializers.Field):
    def field_to_native(self, obj, field_name):
        val = get_component(obj, self.source) or ''
        if self.context.has_key('request') \
                and self.context['request'].user.username.find('ios') != -1:
            return val.replace('+', '')
        else:
            return val

def get_component(obj, attr_name):
    if isinstance(obj, dict):
        val = obj.get(attr_name)
    else:
        val = getattr(obj, attr_name)
    return val

class MiniBusinessSerializer(serializers.ModelSerializer):
    bizId = serializers.Field(source='bizId')
    address = CharSerializer(source='address')
    city = CharSerializer(source='admin3_name')
    state = CharSerializer(source='admin1_code')
    county = CharSerializer(source='admin2_name')
    postalcode = CharSerializer(source='postalcode')
    country = CharSerializer(source='country')
    phone = PhoneSerializer(source='phone')
    website = CharSerializer(source='website')

    categories = JsonSerializer(source='category_json', islist=True)
    social = JsonSerializer(source='social_json', islist=True)
    profile_image = JsonSerializer(source='mobile_image_json')
    square_image = JsonSerializer(source='landing_image_json')
    distance = DistanceField(source='*')
    bounded = serializers.BooleanField()
    location = PointField()

    class Meta:
        model = Business
        fields = ('bizId',
                  'name',
                  'categories',
                  'social',
                  'profile_image',
                  'square_image',
                  'website',
                  'address',
                  'city',
                  'state', 
                  'county',
                  'postalcode',
                  'country',
                  'phone',
                  'location', 
                  'distance', 
                  'has_bitcoin_discount', 
                  )

class PaginatedMiniBizSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = MiniBusinessSerializer

class BusinessSerializer(serializers.ModelSerializer):
    bizId = serializers.Field(source='bizId')
    address = CharSerializer(source='address')
    city = CharSerializer(source='admin3_name')
    state = CharSerializer(source='admin1_code')
    county = CharSerializer(source='admin2_name')
    postalcode = CharSerializer(source='postalcode')
    country = CharSerializer(source='country')
    phone = PhoneSerializer(source='phone')
    website = CharSerializer(source='website')

    profile_image = JsonSerializer(source='mobile_image_json')
    square_image = JsonSerializer(source='landing_image_json')
    images = JsonSerializer(source='images_json', islist=True)
    hours = JsonSerializer(source='hours_json', islist=True)
    categories = JsonSerializer(source='category_json', islist=True)
    social = JsonSerializer(source='social_json', islist=True)
    location = PointField()
    distance = DistanceField(source='*')

    class Meta:
        model = Business
        fields = ('bizId',
                  'name',
                  'categories',
                  'social',
                  'profile_image',
                  'square_image',
                  'images',
                  'description',
                  'website',
                  'phone',
                  'address',
                  'city',
                  'county',
                  'state', 
                  'postalcode',
                  'country',
                  'hours',
                  'has_physical_business', 
                  'has_online_business',
                  'has_bitcoin_discount', 
                  'distance', 
                  'location', )


class AutoCompleteSerializer(serializers.Serializer):
    bizId = serializers.Field(source='pk')
    name = serializers.CharField(required=False, max_length=100)

class AutoCompleteLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoNameZip
        fields = ('admin_name2',
                  'admin_code1',
                 )

class SearchObject(object):
    def __init__(self, term=None, location=None, ll=None, radius=None, bounds=None, category=None, since=None, sort=None):
        self.term=term
        self.location=location
        self.ll=ll
        self.radius=radius
        self.bounds=bounds
        self.category=category
        self.since=since
        self.sort=sort

class SearchSerializer(serializers.Serializer):
    term=serializers.CharField(required=False)
    location=serializers.CharField(required=False)
    ll=serializers.CharField(required=False)
    radius=serializers.CharField(required=False)
    bounds=serializers.CharField(required=False)
    category=serializers.CharField(required=False)
    since=serializers.DateTimeField(required=False)
    sort=serializers.CharField(required=False)

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.l1 = attrs.get('l1', instance.l1)
            instance.term = attrs.get('term', instance.term)
            instance.location = attrs.get('location', instance.location)
            instance.ll = attrs.get('ll', instance.ll)
            instance.radius = attrs.get('radius', instance.radius)
            instance.bounds = attrs.get('bounds', instance.bounds)
            instance.category = attrs.get('category', instance.category)
            instance.since = attrs.get('since', instance.since)
            instance.sort = attrs.get('sort', instance.sort)
            return instance
        return SearchObject(**attrs)


