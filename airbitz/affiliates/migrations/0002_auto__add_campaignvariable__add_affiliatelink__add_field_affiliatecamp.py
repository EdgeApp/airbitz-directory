# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CampaignVariable'
        db.create_table(u'affiliates_campaignvariable', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['affiliates.AffiliateCampaign'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('key_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'affiliates', ['CampaignVariable'])

        # Adding model 'AffiliateLink'
        db.create_table(u'affiliates_affiliatelink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ip_address', self.gf('django.db.models.fields.CharField')(max_length=30, db_index=True)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['affiliates.AffiliateCampaign'])),
        ))
        db.send_create_signal(u'affiliates', ['AffiliateLink'])

        # Adding field 'AffiliateCampaign.payment_address'
        db.add_column(u'affiliates_affiliatecampaign', 'payment_address',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'CampaignVariable'
        db.delete_table(u'affiliates_campaignvariable')

        # Deleting model 'AffiliateLink'
        db.delete_table(u'affiliates_affiliatelink')

        # Deleting field 'AffiliateCampaign.payment_address'
        db.delete_column(u'affiliates_affiliatecampaign', 'payment_address')


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
            'payment_address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'affiliates.affiliatelink': {
            'Meta': {'object_name': 'AffiliateLink'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['affiliates.AffiliateCampaign']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'})
        },
        u'affiliates.campaignvariable': {
            'Meta': {'object_name': 'CampaignVariable'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['affiliates.AffiliateCampaign']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'key_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['affiliates']