# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'HBitsPromos.zero_message'
        db.add_column(u'notifications_hbitspromos', 'zero_message',
                      self.gf('django.db.models.fields.TextField')(default='Sorry. You are too late. The hidden bits have already been claimed. Would you like to tweet anyway?'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'HBitsPromos.zero_message'
        db.delete_column(u'notifications_hbitspromos', 'zero_message')


    models = {
        u'notifications.hbitspromos': {
            'Meta': {'object_name': 'HBitsPromos'},
            'claimed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            'tweet': ('django.db.models.fields.TextField', [], {}),
            'zero_message': ('django.db.models.fields.TextField', [], {})
        },
        u'notifications.notification': {
            'Meta': {'object_name': 'Notification'},
            'android_build_first': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'android_build_last': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ios_build_first': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ios_build_last': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['notifications']