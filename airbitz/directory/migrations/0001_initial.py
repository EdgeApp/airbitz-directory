# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'directory_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2500, null=True)),
        ))
        db.send_create_signal(u'directory', ['Category'])

        # Adding model 'Business'
        db.create_table(u'directory_business', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='DR', max_length=5)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=2000, null=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('postalcode', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['directory.Category'], null=True)),
            ('landing_image', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='landing_image_business', null=True, on_delete=models.SET_NULL, to=orm['directory.BusinessImage'])),
            ('has_physical_business', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_online_business', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_bitcoin_discount', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('center', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True)),
        ))
        db.send_create_signal(u'directory', ['Business'])

        # Adding model 'SocialId'
        db.create_table(u'directory_socialid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('business', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['directory.Business'])),
            ('social_type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('social_id', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('social_url', self.gf('django.db.models.fields.URLField')(max_length=2000, null=True)),
        ))
        db.send_create_signal(u'directory', ['SocialId'])

        # Adding model 'BusinessImage'
        db.create_table(u'directory_businessimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=5000)),
            ('business', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['directory.Business'])),
            ('height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'directory', ['BusinessImage'])

        # Adding model 'BusinessHours'
        db.create_table(u'directory_businesshours', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('business', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['directory.Business'])),
            ('dayOfWeek', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('hourStart', self.gf('django.db.models.fields.TimeField')()),
            ('hourEnd', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal(u'directory', ['BusinessHours'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'directory_category')

        # Deleting model 'Business'
        db.delete_table(u'directory_business')

        # Deleting model 'SocialId'
        db.delete_table(u'directory_socialid')

        # Deleting model 'BusinessImage'
        db.delete_table(u'directory_businessimage')

        # Deleting model 'BusinessHours'
        db.delete_table(u'directory_businesshours')


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