# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Affiliate'
        db.create_table(u'affiliates_affiliate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('bitid_address', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'affiliates', ['Affiliate'])

        # Adding model 'AffiliateCampaign'
        db.create_table(u'affiliates_affiliatecampaign', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('affiliate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['affiliates.Affiliate'])),
            ('token', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal(u'affiliates', ['AffiliateCampaign'])


    def backwards(self, orm):
        # Deleting model 'Affiliate'
        db.delete_table(u'affiliates_affiliate')

        # Deleting model 'AffiliateCampaign'
        db.delete_table(u'affiliates_affiliatecampaign')


    models = {
        u'affiliates.affiliate': {
            'Meta': {'object_name': 'Affiliate'},
            'bitid_address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'affiliates.affiliatecampaign': {
            'Meta': {'object_name': 'AffiliateCampaign'},
            'affiliate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['affiliates.Affiliate']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['affiliates']