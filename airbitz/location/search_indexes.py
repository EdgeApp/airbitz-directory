from haystack import indexes

from location.models import LocationString, OsmRelation

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
    postalcode = indexes.CharField(model_attr='postalcode', null=True)
    country = indexes.CharField(model_attr='country_code', null=True)
    location = indexes.LocationField(model_attr='center', null=True)

    content_auto = indexes.EdgeNgramField(model_attr='content_auto')

    def get_model(self):
        return LocationString


class OsmRelationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='name')
    osm_id = indexes.CharField(model_attr='osm_id', null=True)
    location = indexes.LocationField(model_attr='centroid', null=True)

    def get_model(self):
        return OsmRelation



