from django.db.models import Max
from rest_framework import fields
from rest_framework import pagination
from rest_framework import serializers

from directory.models import Business, BusinessImage, Category
from location.models import GeoNameZip

import json

class SizedImageField(serializers.Field):
    def field_to_native(self, obj, field_name):
        if obj.mobile_image_json:
            return json.loads(obj.mobile_image_json)
        else:
            return {}

class WebImageField(serializers.Field):
    def field_to_native(self, obj, field_name):
        if obj.landing_image_json:
            return json.loads(obj.landing_image_json)
        else:
            return {}

class HoursField(serializers.Field):
    def serial(self, obj):
        return {
            'dayOfWeek': obj.lookupDayOfWeek,
            'hourStart': obj.hourStart,
            'hourEnd': obj.hourEnd 
        }

    def field_to_native(self, obj, field_name):
        ls = obj.businesshours_set.all()
        ls = sorted(ls, lambda x, y: x.lookupDayNumber - y.lookupDayNumber) 
        return [self.serial(t) for t in ls]

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
        if obj.center:
            return {'latitude': obj.center.y, 'longitude': obj.center.x}
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

class CategorySerializer(serializers.Field):
    def field_to_native(self, obj, field_name):
        if obj.category_json:
            return json.loads(obj.category_json)
        else:
            return []

class SocialSerializer(serializers.Field):
    def field_to_native(self, obj, field_name):
        if obj.social_json:
            return json.loads(obj.social_json)
        else:
            return []

class MiniBusinessSerializer(serializers.ModelSerializer):
    bizId = serializers.Field(source='bizId')
    categories = CategorySerializer(source='*')
    social = SocialSerializer(source='socialid_set')
    profile_image = SizedImageField(source='*')
    square_image = WebImageField(source='*')
    state = serializers.CharField(source='admin1_code')
    county = serializers.CharField(source='admin2_name')
    city = serializers.CharField(source='admin3_name')
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
                  'phone',
                  'address',
                  'city',
                  'county',
                  'state', 
                  'postalcode',
                  'country',
                  'location', 
                  'distance', 
                  'has_bitcoin_discount', 
                  )

class PaginatedMiniBizSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = MiniBusinessSerializer

class BusinessSerializer(serializers.ModelSerializer):
    bizId = serializers.Field(source='bizId')
    state = serializers.CharField(source='admin1_code')
    county = serializers.CharField(source='admin2_name')
    city = serializers.CharField(source='admin3_name')
    profile_image = SizedImageField(source='*')
    square_image = WebImageField(source='*')
    images = BusinessImageSerializer(source='businessimage_set')
    hours = HoursField(source='*')
    categories = CategorySerializer(source='*')
    social = SocialSerializer(source='socialid_set')
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

