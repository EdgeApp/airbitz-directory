from haystack import indexes

from location.models import LocationString

class LocationStringIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    admin1_code = indexes.CharField(model_attr='admin1_code', null=True)
    admin1_name = indexes.CharField(model_attr='admin1_name', null=True)
    admin2_code = indexes.CharField(model_attr='admin2_code', null=True)
    admin2_name = indexes.CharField(model_attr='admin2_name', null=True)
    admin3_code = indexes.CharField(model_attr='admin3_code', null=True)
    admin3_name = indexes.CharField(model_attr='admin3_name', null=True)
    admin4_code = indexes.CharField(model_attr='admin4_code', null=True)
    admin4_name = indexes.CharField(model_attr='admin4_name', null=True)
    postalcode = indexes.CharField(model_attr='postalcode')
    location = indexes.LocationField(model_attr='center', null=True)

    def get_model(self):
        return LocationString


