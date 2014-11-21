# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Notification.android_build'
        db.delete_column(u'notifications_notification', 'android_build')

        # Deleting field 'Notification.ios_build'
        db.delete_column(u'notifications_notification', 'ios_build')

        # Adding field 'Notification.ios_build_last'
        db.add_column(u'notifications_notification', 'ios_build_last',
                      self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Notification.ios_build_first'
        db.add_column(u'notifications_notification', 'ios_build_first',
                      self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Notification.android_build_last'
        db.add_column(u'notifications_notification', 'android_build_last',
                      self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Notification.android_build_first'
        db.add_column(u'notifications_notification', 'android_build_first',
                      self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Notification.android_build'
        db.add_column(u'notifications_notification', 'android_build',
                      self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Notification.ios_build'
        db.add_column(u'notifications_notification', 'ios_build',
                      self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Notification.ios_build_last'
        db.delete_column(u'notifications_notification', 'ios_build_last')

        # Deleting field 'Notification.ios_build_first'
        db.delete_column(u'notifications_notification', 'ios_build_first')

        # Deleting field 'Notification.android_build_last'
        db.delete_column(u'notifications_notification', 'android_build_last')

        # Deleting field 'Notification.android_build_first'
        db.delete_column(u'notifications_notification', 'android_build_first')


    models = {
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