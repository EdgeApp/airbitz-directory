# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ImageTag'
        db.create_table(u'directory_imagetag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2500, null=True)),
        ))
        db.send_create_signal(u'directory', ['ImageTag'])

        # Adding M2M table for field tags on 'BusinessImage'
        m2m_table_name = db.shorten_name(u'directory_businessimage_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('businessimage', models.ForeignKey(orm[u'directory.businessimage'], null=False)),
            ('imagetag', models.ForeignKey(orm[u'directory.imagetag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['businessimage_id', 'imagetag_id'])


    def backwards(self, orm):
        # Deleting model 'ImageTag'
        db.delete_table(u'directory_imagetag')

        # Removing M2M table for field tags on 'BusinessImage'
        db.delete_table(db.shorten_name(u'directory_businessimage_tags'))


    models = {
        u'directory.business': {
            'Meta': {'object_name': 'Business'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'admin1_code': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'admin2_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'admin3_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['directory.Category']", 'symmetrical': 'False', 'blank': 'True'}),
            'center': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'has_bitcoin_discount': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_online_business': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_physical_business': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'landing_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'landing_image_business'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['directory.BusinessImage']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'postalcode': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
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
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['directory.ImageTag']", 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        },
        u'directory.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2500', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'social_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'social_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'social_url': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'null': 'True'})
        }
    }

    complete_apps = ['directory']