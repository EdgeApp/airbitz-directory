# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'statistics_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('event_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('event_text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'statistics', ['Event'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'statistics_event')


    models = {
        u'statistics.event': {
            'Meta': {'object_name': 'Event'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event_text': ('django.db.models.fields.TextField', [], {}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['statistics']