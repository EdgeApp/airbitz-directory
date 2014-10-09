from haystack import indexes

import json

from directory.models import Business, Category, SocialId

class BusinessIndex(indexes.SearchIndex, indexes.Indexable):
    bizId = indexes.IntegerField(model_attr='pk', indexed=False)
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name', boost=1.2)
    description = indexes.CharField(model_attr='description', null=True)
    country = indexes.CharField(model_attr='country', null=True)
    admin1_code = indexes.CharField(model_attr='admin1_code', null=True)
    admin2_name = indexes.CharField(model_attr='admin2_name', null=True)

    categories = indexes.MultiValueField()

    category_json = indexes.CharField(null=True, indexed=False)
    mobile_image_json = indexes.CharField(null=True, indexed=False)
    landing_image_json = indexes.CharField(null=True, indexed=False)
    social_json = indexes.CharField(null=True, indexed=False)

    location = indexes.LocationField(model_attr='center', null=True)

    has_physical_business = indexes.BooleanField(model_attr='has_physical_business', null=True)
    has_online_business = indexes.BooleanField(model_attr='has_online_business', null=True)
    has_bitcoin_discount = indexes.DecimalField(model_attr='has_bitcoin_discount', null=True)

    content_auto = indexes.EdgeNgramField(model_attr='name')

    def prepare(self, obj):
        data = super(BusinessIndex, self).prepare(obj)
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
        image = obj.landing_image
        return json.dumps({
                'image': image.mobile_photo.url,
                'width': image.mobile_photo.width,
                'height': image.mobile_photo.height,
                'bounding_box': {'x': 0.0, 'y': 0.0, 'height': 0.25, 'width': 1.0},
                'thumbnail': image.mobile_thumbnail.url})

    def prepare_mobile_image_json(self, obj):
        if not obj.mobile_landing_image:
            return {}
        image = obj.mobile_landing_image
        return json.dumps({
                'image': image.web_photo.url,
                'width': image.web_photo.width,
                'height': image.web_photo.height,
                'bounding_box': {'x': 0.0, 'y': 0.0, 'height': 0.25, 'width': 1.0},
                'thumbnail': image.web_photo.url})

    def prepare_social_json(self, obj):
        ls = []
        for s in SocialId.objects.filter(business=obj):
            ls.append({'social_type': s.social_type,
                       'social_id': s.social_id,
                       'social_url': s.social_url})
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


