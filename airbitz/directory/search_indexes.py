from haystack import indexes

import json

from directory.models import Business, BusinessHours, BusinessImage, Category, SocialId

class BusinessIndex(indexes.SearchIndex, indexes.Indexable):
    bizId = indexes.IntegerField(model_attr='pk', indexed=False)
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name', boost=1.2)
    description = indexes.CharField(model_attr='description', null=True)

    website = indexes.CharField(model_attr='website')
    address = indexes.CharField(model_attr='address')
    phone = indexes.CharField(model_attr='phone')
    postalcode = indexes.CharField(model_attr='postalcode')

    country = indexes.CharField(model_attr='country')
    admin1_code = indexes.CharField(model_attr='admin1_code')
    admin2_name = indexes.CharField(model_attr='admin2_name')
    admin3_name = indexes.CharField(model_attr='admin3_name')

    categories = indexes.MultiValueField()

    category_json = indexes.CharField(null=True, indexed=False)
    mobile_image_json = indexes.CharField(null=True, indexed=False)
    landing_image_json = indexes.CharField(null=True, indexed=False)
    social_json = indexes.CharField(null=True, indexed=False)
    hours_json = indexes.CharField(null=True, indexed=False)
    images_json = indexes.CharField(null=True, indexed=False)

    location = indexes.LocationField(model_attr='center', null=True)

    has_physical_business = indexes.BooleanField(model_attr='has_physical_business', null=True)
    has_online_business = indexes.BooleanField(model_attr='has_online_business', null=True)
    has_bitcoin_discount = indexes.DecimalField(model_attr='has_bitcoin_discount', null=True)

    content_auto = indexes.EdgeNgramField(model_attr='name')

    def prepare(self, obj):
        data = super(BusinessIndex, self).prepare(obj)
        data['bizId'] = obj.pk

        minLevel = min([c.level for c in obj.categories.all()], 0)
        if minLevel >= 1:
            data['boost'] = (1.0 + (1.0 / minLevel))
        return data

    def prepare_categories(self, obj):
        return [category.name for category in obj.categories.all()]

    def prepare_category_json(self, obj):
        return json.dumps([{'name': c.name,
                            'level': c.level} for c in obj.categories.all()])

    def prepare_landing_image_json(self, obj):
        if not obj.landing_image:
            return {}
        return json.dumps(self.serialize_image(obj.landing_image.mobile_photo))

    def prepare_mobile_image_json(self, obj):
        if not obj.mobile_landing_image:
            return {}
        return json.dumps(self.serialize_image(obj.mobile_landing_image.web_photo))

    def prepare_images_json(self, obj):
        ls = []
        for b in BusinessImage.objects.filter(business=obj):
            tags = [t.name for t in b.tags.all()]
            ls.append({
                'image': b.mobile_photo.url,
                'height': b.mobile_photo.height,
                'width': b.mobile_photo.width,
                'thumbnail': b.mobile_thumbnail.url,
                'bounding_box': {'x': 0.0, 'y': 0.0, 'height': 0.25, 'width': 1.0},
                'tags': tags })
        return json.dumps(ls)

    def serialize_image(self, image):
        return { 'image': image.url,
                 'width': image.width,
                 'height': image.height,
                 'bounding_box': {'x': 0.0, 'y': 0.0, 'height': 0.25, 'width': 1.0},
                 'thumbnail': image.url }

    def prepare_social_json(self, obj):
        ls = []
        for s in SocialId.objects.filter(business=obj):
            ls.append({'social_type': s.social_type,
                       'social_id': s.social_id,
                       'social_url': s.social_url})
        return json.dumps(ls)

    def prepare_hours_json(self, obj):
        ls = []
        for s in BusinessHours.objects.filter(business=obj):
            ls.append({'dayOfWeek': s.lookupDayOfWeek,
                       'dayNumber': s.lookupDayNumber,
                       'hourStart': str(s.hourStart),
                       'hourEnd': str(s.hourEnd)})
        ls = sorted(ls, lambda x, y: x['dayNumber'] - y['dayNumber']) 
        return json.dumps(ls)

    def get_model(self):
        return Business

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(status='PUB')


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(model_attr='name', document=True)
    content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Category


