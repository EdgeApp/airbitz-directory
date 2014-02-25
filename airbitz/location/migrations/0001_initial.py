# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LocationString'
        db.create_table(u'location_locationstring', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('neighborhood', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('admin1_code', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('admin1_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('admin2_code', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('admin2_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('admin3_code', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('admin3_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('admin4_code', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('admin4_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('postalcode', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('country_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('content_auto', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('center', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True)),
        ))
        db.send_create_signal(u'location', ['LocationString'])

        # Adding model 'GeoName'
        db.create_table(u'location_geoname', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geonameid', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('asciiname', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('alternatenames', self.gf('django.db.models.fields.CharField')(max_length=5000)),
            ('feature_class', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('feature_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('country_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('cc2', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('admin1_code', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('admin2_code', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('admin3_code', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('admin4_code', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('population', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('elevation', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('dem', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('timezone', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('modification_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('center', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True)),
        ))
        db.send_create_signal(u'location', ['GeoName'])

        # Adding model 'GeoNameZip'
        db.create_table(u'location_geonamezip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('postalcode', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('place_name', self.gf('django.db.models.fields.CharField')(max_length=180)),
            ('admin_name1', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('admin_code1', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('admin_name2', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('admin_code2', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('admin_name3', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('accuracy', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('center', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True)),
        ))
        db.send_create_signal(u'location', ['GeoNameZip'])


    def backwards(self, orm):
        # Deleting model 'LocationString'
        db.delete_table(u'location_locationstring')

        # Deleting model 'GeoName'
        db.delete_table(u'location_geoname')

        # Deleting model 'GeoNameZip'
        db.delete_table(u'location_geonamezip')


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
        }
    }

    complete_apps = ['location']