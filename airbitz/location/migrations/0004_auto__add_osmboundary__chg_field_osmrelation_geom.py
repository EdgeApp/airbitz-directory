# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OsmBoundary'
        db.create_table(u'location_osmboundary', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('osm_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('geom', self.gf('django.contrib.gis.db.models.fields.GeometryField')()),
        ))
        db.send_create_signal(u'location', ['OsmBoundary'])


        # Changing field 'OsmRelation.geom'
        db.alter_column(u'location_osmrelation', 'geom', self.gf('django.contrib.gis.db.models.fields.GeometryField')(null=True))

    def backwards(self, orm):
        # Deleting model 'OsmBoundary'
        db.delete_table(u'location_osmboundary')


        # Changing field 'OsmRelation.geom'
        db.alter_column(u'location_osmrelation', 'geom', self.gf('django.contrib.gis.db.models.fields.GeometryField')(default=None))

    models = {
        u'location.geoname': {
            'Meta': {'object_name': 'GeoName'},
            'admin1_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'admin2_code': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'admin3_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'admin4_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'alternatenames': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'asciiname': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'cc2': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'center': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'dem': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'elevation': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'feature_class': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'feature_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'geonameid': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'population': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'})
        },
        u'location.geonamezip': {
            'Meta': {'object_name': 'GeoNameZip'},
            'accuracy': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'admin_code1': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'admin_code2': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'admin_name1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'admin_name2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'admin_name3': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'center': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place_name': ('django.db.models.fields.CharField', [], {'max_length': '180'}),
            'postalcode': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        u'location.locationstring': {
            'Meta': {'object_name': 'LocationString'},
            'admin1_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'admin1_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'admin2_code': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'admin2_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'admin3_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'admin3_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'admin4_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'admin4_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'center': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'content_auto': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'postalcode': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'location.osmboundary': {
            'Meta': {'object_name': 'OsmBoundary'},
            'geom': ('django.contrib.gis.db.models.fields.GeometryField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'osm_id': ('django.db.models.fields.BigIntegerField', [], {})
        },
        u'location.osmrelation': {
            'Meta': {'object_name': 'OsmRelation'},
            'admin_level': ('django.db.models.fields.SmallIntegerField', [], {}),
            'centroid': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'geom': ('django.contrib.gis.db.models.fields.GeometryField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'osm_id': ('django.db.models.fields.BigIntegerField', [], {})
        }
    }

    complete_apps = ['location']