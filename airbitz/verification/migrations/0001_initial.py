# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MailVerify'
        db.create_table(u'verification_mailverify', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('verify_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('verify_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('mail', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'verification', ['MailVerify'])


    def backwards(self, orm):
        # Deleting model 'MailVerify'
        db.delete_table(u'verification_mailverify')


    models = {
        u'verification.mailverify': {
            'Meta': {'object_name': 'MailVerify'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'verify_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'verify_id': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['verification']