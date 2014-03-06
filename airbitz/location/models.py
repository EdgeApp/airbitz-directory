from django.contrib.gis.db import models

class LocationString(models.Model):
    neighborhood = models.CharField(max_length=200)
    admin1_code = models.CharField(max_length=20, null=True)
    admin1_name = models.CharField(max_length=200, null=True)
    admin2_code = models.CharField(max_length=80, null=True)
    admin2_name = models.CharField(max_length=200, null=True)
    admin3_code = models.CharField(max_length=20, null=True)
    admin3_name = models.CharField(max_length=200, null=True)
    admin4_code = models.CharField(max_length=20, null=True)
    admin4_name = models.CharField(max_length=200, null=True)
    postalcode = models.CharField(max_length=20)
    country_code = models.CharField(max_length=20)
    content_auto = models.CharField(max_length=200, unique=True)
    center = models.PointField(null=True)
    objects = models.GeoManager()

class OsmRelation(models.Model):
    osm_id = models.BigIntegerField()
    admin_level = models.SmallIntegerField()
    name = models.CharField(max_length=2000)
    country_code = models.CharField(max_length=20)
    geom = models.GeometryField(null=False)
    centroid = models.PointField(null=False)
    objects = models.GeoManager()

class GeoName(models.Model):
    geonameid = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    asciiname = models.CharField(max_length=200)
    alternatenames = models.CharField(max_length=5000)
    feature_class = models.CharField(max_length=1)
    feature_code = models.CharField(max_length=10)
    country_code = models.CharField(max_length=10)
    cc2 = models.CharField(max_length=60)
    admin1_code = models.CharField(max_length=20, null=True)
    admin2_code  =  models.CharField(max_length=80, null=True)
    admin3_code = models.CharField(max_length=20, null=True)
    admin4_code  =  models.CharField(max_length=20, null=True)
    population = models.IntegerField(null=True)
    elevation  =  models.IntegerField(null=True)
    dem = models.IntegerField(null=True)
    timezone = models.CharField(max_length=40, null=True)
    modification_date = models.DateField(null=True)

    center = models.PointField(null=True)
    objects = models.GeoManager()


class GeoNameZip(models.Model):
    country = models.CharField(max_length=2)
    postalcode = models.CharField(max_length=20, unique=True)
    place_name = models.CharField(max_length=180)
    admin_name1 = models.CharField(max_length=100) # state
    admin_code1 = models.CharField(max_length=20)
    admin_name2 = models.CharField(max_length=100, null=True) # county/province
    admin_code2 = models.CharField(max_length=20, null=True)
    admin_name3 = models.CharField(max_length=100, null=True) # community
    accuracy = models.IntegerField(null=True) # accuracy of lat/lng from 1=estimated to 6=centroid
    center = models.PointField(null=True)
    objects = models.GeoManager()


