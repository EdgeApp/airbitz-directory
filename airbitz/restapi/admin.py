from django.contrib.gis.geos import Point, Polygon
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models import Q
from rest_framework import authentication as auth
from rest_framework import fields
from rest_framework import pagination
from rest_framework import serializers
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, UpdateAPIView, \
    ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

import logging
import datetime
from rest_framework.views import APIView
from airbitz import settings
from airbitz import regions_data

from directory.models import Business, BusinessHours, Category, SocialId, ThirdPartyBusiness, ThirdPartyBusinessImage, \
    ThirdPartyBusinessImageTag, ThirdPartyCategory, ExpenseCategory
from restapi import api

log = logging.getLogger("airbitz." + __name__)

DEFAULT_PAGE_SIZE = 20

PERMS = (auth.SessionAuthentication,)

def parseGeoBounds(bounds):
    if not bounds:
        return None
    try:
        (sw,ne) = bounds.split("|")
        sw = sw.split(",")
        ne = ne.split(",")
        box = {
            'minlat': float(sw[0]),
            'minlon': float(sw[1]),
            'maxlat': float(ne[0]),
            'maxlon': float(ne[1]),
        }
        return Polygon.from_bbox((box['minlon'], box['minlat'], box['maxlon'], box['maxlat']))
    except Exception as e:
        log.warn(e)
        raise api.AirbitzApiException('Unable to parse geographic bounds.')

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
        if obj:
            return {'latitude': obj.y, 'longitude': obj.x}
        else:
            return None

    def from_native(self, data):
        if data['longitude'] and data['latitude']:
            return Point((data['longitude'], data['latitude']))
        else:
            return None

class AdminCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', )

class AdminSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialId
        fields = ('id', 'social_type', 'social_id', 'social_url')

class AdminHoursSerializer(serializers.ModelSerializer):
    hourStart = fields.CharField(required=False);
    hourEnd = fields.CharField(required=False);
    class Meta:
        model = BusinessHours
        fields = ('id', 'dayOfWeek','hourStart', 'hourEnd', )

class AdminBizImageSerializer(serializers.ModelSerializer):
    id = fields.IntegerField();
    image = fields.CharField(source='admin_photo.url')
    width = fields.IntegerField(source='admin_photo.width')
    height = fields.IntegerField(source='admin_photo.height')

    mobile_photo_x1 = fields.CharField(source='mobile_photo_x1', required=False)
    mobile_photo_y1 = fields.CharField(source='mobile_photo_y1', required=False)
    mobile_photo_x2 = fields.CharField(source='mobile_photo_x2', required=False)
    mobile_photo_y2 = fields.CharField(source='mobile_photo_y2', required=False)

    web_photo_x1 = fields.CharField(source='web_photo_x1', required=False)
    web_photo_y1 = fields.CharField(source='web_photo_y1', required=False)
    web_photo_x2 = fields.CharField(source='web_photo_x2', required=False)
    web_photo_y2 = fields.CharField(source='web_photo_y2', required=False)

    class Meta:
        model = BusinessHours
        fields = ('id', 'image', 'height', 'width', 
                  'mobile_photo_x1', 'mobile_photo_y1', 
                  'mobile_photo_x2', 'mobile_photo_y2',
                  'web_photo_x1', 'web_photo_y1', 
                  'web_photo_x2', 'web_photo_y2',  )

class AdminBizSerializer(serializers.ModelSerializer):
    categories = AdminCategorySerializer(source='categories', many=True)
    hours = AdminHoursSerializer(source='businesshours_set', many=True)
    images = AdminBizImageSerializer(source='businessimage_set', many=True)
    social = AdminSocialSerializer(source='socialid_set', many=True)
    center = AdminPointField(source='center', required=False)

    class Meta:
        model = Business

class AdminCategory(ListCreateAPIView):
    serializer_class = AdminCategorySerializer
    filter_fields = ('name', )
    permission_classes = (IsAdminUser,)
    authentication_classes = PERMS
    model = Category
    paginate_by = 1000

class AdminCategoryDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = AdminCategorySerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = PERMS
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

class ScreencapList(ListCreateAPIView):
    serializer_class = AdminBizSerializer
    model = Business
    allow_empty = True

    def get_queryset(self):
        interval = settings.SCREENCAP_INTERVAL
        date1 = datetime.datetime.today()
        date2 = date1 - interval
        q = Business.objects.filter(status="PUB").filter(modified__lte=date1, modified__gte=date2)
        return q

class AdminBusinessView(ListCreateAPIView):
    serializer_class = AdminBizSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = PERMS
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

    def paramSearchArray(self, request):
        totalColumns = int(self.request.QUERY_PARAMS.get('iColumns', '0'))
        search = 'sSearch_'
        l = []

        i = 0
        for i in xrange(0, totalColumns):
            l.append(request.QUERY_PARAMS.get(search + str(i)))

        return  l

    def formatDir(self, c, d):
        if d == "desc":
            return '-' + c
        else:
            return c

    def get_queryset(self):
        search = self.request.QUERY_PARAMS.get('sSearch', None)
        location = self.request.QUERY_PARAMS.get('adminLocation', None)
        bounds = self.request.QUERY_PARAMS.get('bounds', None)
        bizStatus = self.request.QUERY_PARAMS.get('status', None)
        cols = self.paramArray('mDataProp_', self.request)
        sorts = self.paramArray('iSortCol_', self.request)
        dirs = self.paramArray('sSortDir_', self.request)
        filters = self.paramSearchArray(request=self.request)
        col_filters = zip(cols, filters)

        print ''
        print '--- SEARCH -----------------------------'
        print search
        print ''
        print '--- LOCATION -----------------------------'
        print location
        print ''
        print '--- STATUS -----------------------------'
        print bizStatus
        print ''
        print '--- COLS -----------------------------'
        print cols
        print ''
        print '--- SORTS -----------------------------'
        print sorts
        print ''
        print '--- DIRS -----------------------------'
        print dirs
        print ''

        if any(filters):
            print '--- FILTERS -----------------------------'
            print filters
            print ''
            print '--- COLS, FILTERS -----------------------------'
            for row in col_filters:
                print row
            print ''
        else:
            print '--- NO FILTERS DETECTED ---'
            print ''


        q = Business.objects.all()

        if any(filters):
            for c,f in col_filters:
                if f:
                    kwargs = {}
                    if str(c) != 'categories':
                        c = str(c)
                        f = str(f)
                        if f.startswith('!'):
                            kwargs = {'{0}__exact'.format(c): f[1:]}
                        elif f.startswith('#'):
                            kwargs = {'{0}__iexact'.format(c): f[1:]}
                        else:
                            kwargs = {'{0}__icontains'.format(c): f}
                        print '******* ######## ',kwargs
                        q = q.filter(Q(**kwargs))
                    elif str(c) == 'categories':
                        c = str(c)
                        f = str(f)
                        if f.startswith('!'):
                            kwargs = {'categories__name__exact': f[1:]}
                        elif f.startswith('#'):
                            kwargs = {'categories__name__iexact': f[1:]}
                        else:
                            kwargs = {'categories__name__icontains': f}

                        print '******* CATEGORIES ######## ',kwargs
                        q = q.filter(Q(**kwargs))

        if search:
            q = q.filter(
                Q(name__icontains=search) |
                Q(categories__name__icontains=search) |
                Q(description__icontains=search) |
                Q(admin_notes__icontains=search)
            )
            q = q.distinct()
        if location:
            a = api.ApiProcess(locationStr=location)
            if a.location.bounding:
                q = q.filter(center__within=a.location.bounding)
        if bizStatus:
            q = q.filter(status=bizStatus)
        if bounds:
            poly = parseGeoBounds(bounds)
            q = q.filter(center__within=poly)
        if sorts:
            l = []
            for (s, d) in zip(sorts, dirs):
                c = cols[int(s)]
                l.append(self.formatDir(c, d))
            q = q.order_by(*l)
        q = q.annotate(ccount=Count('categories'))
        return q

class AdminBusinessDetails(RetrieveUpdateDestroyAPIView):
    serializer_class = AdminBizSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = PERMS
    model = Business

    def __update_cats__(self, request):
        if request.DATA.has_key('categories'):
            cats = self.object.categories.all()
            delcats = dict((c.id, c) for c in cats)
            for c in request.DATA['categories']:
                if not c.has_key('name') or not c.has_key('id'):
                    continue
                if c['id'] <= 0:
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

    def __update_social__(self, request):
        if request.DATA.has_key('social'):
            socials = self.object.socialid_set.all()
            delsocial = dict((c.id, c) for c in socials)
            print delsocial
            for c in request.DATA['social']:
                print c
                if not c.has_key('id'):
                    continue
                if c['id'] == 0:
                    newsocial = SocialId.objects.create(business=self.object,\
                                                      social_type=c['social_type'],\
                                                      social_id=c['social_id'],\
                                                      social_url=c['social_url'])
                    c['id'] = newsocial.id
                if delsocial.has_key(c['id']):
                    d = delsocial[c['id']]
                    d.social_id = c['social_id']
                    d.social_type = c['social_type']
                    d.social_url = c['social_url']
                    d.save()
                    delsocial.pop(c['id'])
            for i in delsocial.itervalues():
                print 'deleting ', i
                i.delete()

            socialList = []
            self.object = Business.objects.get(id=self.object.id)
            for s in self.object.socialid_set.all():
                serial = AdminSocialSerializer(s)
                socialList.append(serial.data)
            request.DATA['social'] = socialList

    def __update_images__(self, request):
        if request.DATA.has_key('images'):
            imgs = self.object.businessimage_set.all()
            delimg = dict((c.id, c) for c in imgs)
            print delimg
            for c in request.DATA['images']:
                #print c
                if not c.has_key('id'):
                    continue
                if delimg.has_key(c['id']):
                    i = delimg.pop(c['id'])
                    i.mobile_photo_x1 = int(c['mobile_photo_x1'] or 0)
                    i.mobile_photo_y1 = int(c['mobile_photo_y1'] or 0)
                    i.mobile_photo_x2 = int(c['mobile_photo_x2'] or 320)
                    i.mobile_photo_y2 = int(c['mobile_photo_y2'] or 640)
                    i.web_photo_x1 = int(c['web_photo_x1'] or 0)
                    i.web_photo_y1 = int(c['web_photo_y1'] or 0)
                    i.web_photo_x2 = int(c['web_photo_x2'] or 300)
                    i.web_photo_y2 = int(c['web_photo_y2'] or 300)
                    i.save()
                    i.mobile_photo.generate()
                    i.web_photo.generate()

            for i in delimg.itervalues():
                print 'deleting ', i
                i.delete()

            imgList = []
            self.object = Business.objects.get(id=self.object.id)
            for s in self.object.businessimage_set.all():
                serial = AdminBizImageSerializer(s)
                imgList.append(serial.data)
            request.DATA['images'] = imgList

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
        self.__update_social__(request)
        self.__update_images__(request)
        if serializer.is_valid():
            try:
                self.pre_save(serializer.object)
            except ValidationError as err:
                return Response(err.message_dict, status=status.HTTP_400_BAD_REQUEST)
            self.object = serializer.save(**save_kwargs)
            self.post_save(self.object, created=created)
            return Response(serializer.data, status=success_status_code)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




########################################
# REGION QUERIES
########################################
class CountryLabel(serializers.Field):
    def field_to_native(self, obj, field_name):
        country_code = obj['country']
        country_label = obj['country']

        if country_code.lower() == 'US'.lower():
            country_label = 'United States'
        elif country_code.lower() == 'CA'.lower():
            country_label = 'Canada'
        elif country_code.lower() == 'UK'.lower() or country_code.lower() == 'GB'.lower():
            country_label = 'United Kingdom'
        else:
            for ccode, label in regions_data.ALL_COUNTRY_LABELS.items():
                if country_code.lower() == ccode.lower():
                    country_label = label
                    break
                else:
                    country_label = obj['country']

        return country_label


class RegionCountrySerializer(serializers.ModelSerializer):
    country_code = fields.CharField(source='country')
    country_label = CountryLabel(source='country')
    biz_count = fields.IntegerField()

    class Meta:
        model = Business
        fields = ('biz_count', 'country_code', 'country_label',)




class RegionLabel(serializers.Field):
    def field_to_native(self, obj, field_name):
        region_code = obj['admin1_code'].strip()
        country_code = obj['country'].strip()
        # remove periods
        region_code = region_code.replace('.', '')
        country_code = country_code.replace('.', '')

        region_label = ''

        '''
        List any subregions that have been defined for a country code
        '''
        if country_code.upper() == 'US':
            sub_regions = regions_data.US_REGIONS
        elif country_code.upper() == 'CA':
            sub_regions = regions_data.CA_REGIONS
        elif country_code.upper() == 'AU':
            sub_regions = regions_data.AU_REGIONS
        elif country_code.upper() == 'DE':
            sub_regions = regions_data.DE_REGIONS
        elif country_code.upper() == 'NL':
            sub_regions = regions_data.NL_REGIONS
        elif country_code.upper() == 'AR':
            sub_regions = regions_data.AR_REGIONS
        elif country_code.upper() == 'BR':
            sub_regions = regions_data.BR_REGIONS
        elif country_code.upper() == 'CH':
            sub_regions = regions_data.CH_REGIONS
        elif country_code.upper() == 'AT':
            sub_regions = regions_data.AT_REGIONS
        elif country_code.upper() == 'NZ':
            sub_regions = regions_data.NZ_REGIONS
        elif country_code.upper() == 'PH':
            sub_regions = regions_data.PH_REGIONS
        else:
            sub_regions = False

        if sub_regions:
            for rcode, rdata in sub_regions.items():
                if country_code.lower() + '-' + region_code.lower() == rcode.lower():
                    region_label = rdata['name']
                    # print '*************'
                    # print 'MATCHED', rcode, '==', country_code + '-' + region_code
                    # print '*************'
                    break
                else:
                    # print 'NO MATCH', rcode, '!==', country_code + '-' + region_code
                    region_label = obj['admin1_code']
        else:
            region_label = obj['admin1_code']



        return region_label


class RegionDetailsSerializer(serializers.ModelSerializer):
    country_code = fields.CharField(source='country')
    country_label = CountryLabel(source='country')

    region = fields.CharField(source='admin1_code')
    region_label = RegionLabel(source='admin1_code')

    biz_count = fields.IntegerField()

    class Meta:
        model = Business
        fields = ('biz_count', 'region', 'region_label', 'country_code', 'country_label',)




class RegionDetails(ListCreateAPIView):
    serializer_class = RegionDetailsSerializer
    model = Business
    allow_empty = True
    paginate_by = 200

    def get_queryset(self):
        country = self.kwargs['country']
        if country is not None:
            q = Business.objects.filter(status="PUB", country=country)
            q = q.exclude(admin1_code="")
        else:
            q = Business.objects.filter(status="PUB", country='US')

        q = q.values('country', 'admin1_code').annotate(biz_count=Count('admin1_code')).order_by('-biz_count')

        return q


class RegionCountryQuery(ListCreateAPIView):
    serializer_class = RegionCountrySerializer
    model = Business
    allow_empty = True
    paginate_by = 200

    def get_queryset(self):
        country_list = regions_data.get_active_country_codes()

        q = Business.objects.filter(status="PUB", country__in=country_list)
        # q = q.exclude(admin1_code="") # we remove blank cities to prevent confusion when seeing the country total
        q = q.values('country').annotate(biz_count=Count('country')).order_by('-biz_count')

        return q



class MetaResponse(Response):
    def __init__(self, data=None, meta=None, *args, **kwargs):
        newdata = {
            'meta': meta
        }
        if data:
            newdata['results'] = data
        super(MetaResponse, self).__init__(data=newdata, *args, **kwargs)


class PublishedDetailsSerializer(serializers.ModelSerializer):
    country_code = fields.CharField(source='country')
    country_label = CountryLabel(source='country')

    biz_count = fields.IntegerField()

    class Meta:
        model = Business
        fields = ('biz_count', 'country_code', 'country_label',)


class PublishedDetails(ListCreateAPIView):
    serializer_class = PublishedDetailsSerializer
    model = Business
    allow_empty = True

    def get(self, request, *args, **kwargs):

        try:
            interval = datetime.timedelta(days=int(self.kwargs['days']))
        except KeyError:
            interval = settings.FP_QUERY_INTERVAL

        country_list = regions_data.get_active_country_codes()
        date1 = datetime.datetime.today()
        date2 = date1 - interval

        q = Business.objects.filter(status="PUB", country__in=country_list)

        published = q.filter(published__gte=date2)
        updated = q.filter(published__lte=date2, modified__lte=date1, modified__gte=date2)

        country_counts = q.values('country').annotate(biz_count=Count('country')).order_by('-biz_count')


        meta = {
            'biz_total': q.count(),
            'biz_published': published.count(),
            'biz_updated': updated.count(),
        }
        serialized = PublishedDetailsSerializer(data=country_counts)

        return MetaResponse(data=serialized.data, meta=meta)




########################################
# EXTERNAL API (bitpay)
########################################
class ThirdPartyBusinessImageTagSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)


class ThirdPartyBusinessImageSerializer(serializers.Serializer):
    url = serializers.URLField(required=True, max_length=2000)
    tags = ThirdPartyBusinessImageTagSerializer(required=False, source='tags', many=True)


class ThirdPartyCategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)


class ThirdPartyBusinessSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, max_length=200)
    provider_id = serializers.CharField(required=False, max_length=200)
    provider_url = serializers.CharField(required=False, max_length=200)
    website = serializers.URLField(required=False, max_length=2000)
    phone = serializers.CharField(required=False, max_length=200)
    description = serializers.CharField(required=False)
    street_address = serializers.CharField(required=False, max_length=200)
    neighborhood = serializers.CharField(required=False, max_length=200)
    admin3_name = serializers.CharField(required=False, max_length=200)
    admin2_name = serializers.CharField(required=False, max_length=200)
    admin1_code = serializers.CharField(required=False, max_length=200)
    postalcode = serializers.CharField(required=False, max_length=200)
    country = serializers.CharField(required=False, max_length=200)
    physical_business = serializers.CharField(required=False, max_length=200)
    online_business = serializers.CharField(required=False, max_length=200)
    bitcoin_discount = serializers.CharField(required=False, max_length=200)
    score = serializers.CharField(required=False, max_length=200)

    location = AdminPointField(source='location', required=False)
    categories = ThirdPartyCategorySerializer(required=False, source='categories')
    expense_category = serializers.CharField(required=False, max_length=200)
    images = ThirdPartyBusinessImageSerializer(required=False, source='images')


class ThirdPartyBusinessSubmit(APIView):
    serializer_class = ThirdPartyBusinessSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (auth.TokenAuthentication,)
    model = ThirdPartyBusiness

    def find_existing(self, request):
        try:
            return ThirdPartyBusiness.objects.get(user=request.user, provider_id=request.DATA.get('provider_id'))
        except Exception as e:
            print e

        return None

    def populate(self, serializer, request):
        created = False
        instance = self.find_existing(request)

        if instance is None:
            instance = ThirdPartyBusiness.objects.create(
                user=request.user,
                provider_id=request.DATA['provider_id'],
                name=request.DATA['name']
            )
            created = True

        instance.user = request.user
        instance.name = serializer.data.get('name')
        instance.description = serializer.data.get('description')
        instance.website = serializer.data.get('website')
        instance.phone = serializer.data.get('phone', None)
        instance.street_address = serializer.data.get('street_address', None)
        instance.neighborhood = serializer.data.get('neighborhood', None)
        instance.admin3_name = serializer.data.get('admin3_name', None)
        instance.admin2_name = serializer.data.get('admin2_name', None)
        instance.admin1_code = serializer.data.get('admin1_code', None)
        instance.postalcode = serializer.data.get('postalcode', None)
        instance.country = serializer.data.get('country', None)
        instance.physical_business = serializer.data.get('physical_business', None)
        instance.online_business = serializer.data.get('online_business', None)
        instance.bitcoin_discount = serializer.data.get('bitcoin_discount', None)
        instance.score = serializer.data.get('score', None)
        instance.location = self.get_value(serializer, 'location')

        for s in serializer.data.get('categories', []):
            newcat, _ = ThirdPartyCategory.objects.get_or_create(name=s['name'])
            instance.categories.add(newcat)

        if serializer.data.get('expense_category', None):
            newexpcat, _ = ExpenseCategory.objects.get_or_create(name=serializer.data.get('expense_category', None))
            instance.expense_category = newexpcat

        for i in serializer.data.get('images', []):
            newimg, _ = ThirdPartyBusinessImage.objects.get_or_create(url=i['url'], business=instance)

        instance.save()
        return created

    def get_value(self, s, field):
        return s.get_fields().get(field).from_native(s.data.get(field, None))


    def post(self, request):
        serializer = self.serializer_class(data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            # self.pre_save(serializer.object)

            # set pk for update if already exists)
            resp_created = "Feed me more!"
            resp_updated = "Keep it coming!"
            if self.populate(serializer, request):
                return Response(resp_created, status=status.HTTP_201_CREATED)
            else:
                return Response(resp_updated, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

