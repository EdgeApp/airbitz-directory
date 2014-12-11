# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HBitsPromos'
        db.create_table(u'notifications_hbitspromos', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('token', self.gf('django.db.models.fields.CharField')(unique=True, max_length=35)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('tweet', self.gf('django.db.models.fields.TextField')()),
            ('claimed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'notifications', ['HBitsPromos'])


    def backwards(self, orm):
        # Deleting model 'HBitsPromos'
        db.delete_table(u'notifications_hbitspromos')


    models = {
        u'notifications.hbitspromos': {
            'Meta': {'object_name': 'HBitsPromos'},
            'claimed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            'tweet': ('django.db.models.fields.TextField', [], {})
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