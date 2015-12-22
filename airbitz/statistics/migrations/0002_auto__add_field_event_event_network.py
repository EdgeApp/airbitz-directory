# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.event_network'
        db.add_column(u'statistics_event', 'event_network',
                      self.gf('django.db.models.fields.CharField')(default='mainnet', max_length=30),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Event.event_network'
        db.delete_column(u'statistics_event', 'event_network')


    models = {
        u'statistics.event': {
            'Meta': {'object_name': 'Event'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event_network': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'event_text': ('django.db.models.fields.TextField', [], {}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['statistics']