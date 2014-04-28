from haystack import indexes

from directory.models import Business, Category

class BusinessIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name', boost=1.2)
    description = indexes.CharField(model_attr='description', null=True)
    country = indexes.CharField(model_attr='country', null=True)
    admin1_code = indexes.CharField(model_attr='admin1_code', null=True)
    admin2_name = indexes.CharField(model_attr='admin2_name', null=True)

    categories = indexes.MultiValueField()
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

    def get_model(self):
        return Business

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(status='PUB')


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(model_attr='name', document=True)
    content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Category


