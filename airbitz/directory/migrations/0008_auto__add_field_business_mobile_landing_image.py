# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Business.mobile_landing_image'
        db.add_column(u'directory_business', 'mobile_landing_image',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='mobile_landing_image', null=True, on_delete=models.SET_NULL, to=orm['directory.BusinessImage']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Business.mobile_landing_image'
        db.delete_column(u'directory_business', 'mobile_landing_image_id')


    models = {
        u'directory.business': {
            'Meta': {'object_name': 'Business'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'admin1_code': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'admin2_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'admin3_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['directory.Category']", 'null': 'True', 'blank': 'True'}),
            'center': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'has_bitcoin_discount': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '5', 'decimal_places': '3'}),
            'has_online_business': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_physical_business': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'landing_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'landing_image_business'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['directory.BusinessImage']"}),
            'mobile_landing_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mobile_landing_image'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['directory.BusinessImage']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'postalcode': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'DR'", 'max_length': '5'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'})
        },
        u'directory.businesshours': {
            'Meta': {'object_name': 'BusinessHours'},
            'business': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directory.Business']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dayOfWeek': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'hourEnd': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'hourStart': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
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
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['directory.ImageTag']", 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        },
        u'directory.category': {
            'Meta': {'object_name': 'Category'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2500', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'directory.imagetag': {
            'Meta': {'object_name': 'ImageTag'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2500', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'directory.socialid': {
            'Meta': {'object_name': 'SocialId'},
            'business': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directory.Business']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'social_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'social_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'social_url': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['directory']