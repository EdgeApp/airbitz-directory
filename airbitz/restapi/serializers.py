from django.db.models import Max
from rest_framework import fields
from rest_framework import pagination
from rest_framework import serializers

from directory.models import Business, BusinessHours, \
                             BusinessImage, Category, \
                             SocialId
from location.models import GeoNameZip

class SizedImageField(serializers.Field):
    def field_to_native(self, obj, field_name):
        image = obj.landing_image
        if image:
            return {
                'image': image.mobile_photo.url,
                'width': image.mobile_photo.width,
                'height': image.mobile_photo.height,
                'bounding_box': {'x': 0.0, 'y': 0.0, 'height': 0.25, 'width': 1.0},
                'thumbnail': image.mobile_thumbnail.url,
            }
        else:
            return {}

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
        if obj.distance:
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

    class Meta:
        model = BusinessImage
        fields = ('image', 'height', 'width', 'thumbnail', 'bounding_box',)

class BusinessHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessHours
        fields = ('dayOfWeek','hourStart', 'hourEnd', )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'level', )

class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialId
        fields = ('social_type', 'social_id', 'social_url')

class MiniBusinessSerializer(serializers.ModelSerializer):
    bizId = serializers.Field(source='pk')
    categories = CategorySerializer(source='categories')
    social = SocialSerializer(source='socialid_set')
    profile_image = SizedImageField(source='landing_image')
    state = serializers.CharField(source='admin1_code')
    county = serializers.CharField(source='admin2_name')
    city = serializers.CharField(source='admin3_name')
    distance = DistanceField(source='*')
    location = PointField()

    class Meta:
        model = Business
        fields = ('bizId',
                  'name',
                  'categories',
                  'social',
                  'profile_image',
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
    bizId = serializers.Field(source='pk')
    state = serializers.CharField(source='admin1_code')
    county = serializers.CharField(source='admin2_name')
    city = serializers.CharField(source='admin3_name')
    images = BusinessImageSerializer(source='businessimage_set')
    hours = BusinessHoursSerializer(source='businesshours_set')
    categories = CategorySerializer(source='categories')
    social = SocialSerializer(source='socialid_set')
    location = PointField()

    class Meta:
        model = Business
        fields = ('bizId',
                  'name',
                  'categories',
                  'social',
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

