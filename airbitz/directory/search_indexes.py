from haystack import indexes

from directory.models import Business, Category

class BusinessIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    admin1_code = indexes.CharField(model_attr='admin1_code', null=True)
    admin2_name = indexes.CharField(model_attr='admin2_name', null=True)
    admin3_name = indexes.CharField(model_attr='admin3_name', null=True)
    admin3_name = indexes.CharField(model_attr='admin3_name', null=True)
    country = indexes.CharField(model_attr='country', null=True)

    has_physical_business = indexes.BooleanField(model_attr='has_physical_business', null=True)
    has_online_business = indexes.BooleanField(model_attr='has_online_business', null=True)

    content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Business

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(status='PUB')


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(model_attr='name', document=True)
    content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Category


