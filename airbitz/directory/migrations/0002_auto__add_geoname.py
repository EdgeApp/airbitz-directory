# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GeoName'
        db.create_table(u'directory_geoname', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('postalcode', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('place_name', self.gf('django.db.models.fields.CharField')(max_length=180)),
            ('admin_name1', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('admin_code1', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('admin_name2', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('admin_code2', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('admin_name3', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('accuracy', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('center', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True)),
        ))
        db.send_create_signal(u'directory', ['GeoName'])


    def backwards(self, orm):
        # Deleting model 'GeoName'
        db.delete_table(u'directory_geoname')


    models = {
        u'directory.business': {
            'Meta': {'object_name': 'Business'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directory.Category']", 'null': 'True'}),
            'center': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'has_bitcoin_discount': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_online_business': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_physical_business': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'landing_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'landing_image_business'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['directory.BusinessImage']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'postalcode': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'DR'", 'max_length': '5'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'null': 'True'})
        },
        u'directory.businesshours': {
            'Meta': {'object_name': 'BusinessHours'},
            'business': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directory.Business']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dayOfWeek': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'hourEnd': ('django.db.models.fields.TimeField', [], {}),
            'hourStart': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'directory.businessimage': {
            'Meta': {'object_name': 'BusinessImage'},
            'business': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directory.Business']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '5000'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        },
        u'directory.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2500', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'directory.geoname': {
            'Meta': {'object_name': 'GeoName'},
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
            'postalcode': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'directory.socialid': {
            'Meta': {'object_name': 'SocialId'},
            'business': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directory.Business']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'social_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'social_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'social_url': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'null': 'True'})
        }
    }

    complete_apps = ['directory']