from django.contrib.gis.db import models
from django.contrib import admin

class Affiliate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    bitid_address = models.CharField(max_length=100)

class AffiliateCampaign(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    affiliate = models.ForeignKey(Affiliate, null=False, blank=False)
    token = models.CharField(max_length=30, unique=True)
    payment_address = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return "{0}".format(self.token)

class CampaignVariable(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    campaign = models.ForeignKey(AffiliateCampaign, null=False, blank=False)
    key = models.CharField(max_length=30, null=False)
    key_type = models.CharField(max_length=30, null=False)
    value = models.TextField(null=False)

    def __unicode__(self):
        return "{0}".format(self.key, self.key_type, self.key_value)

class AffiliateLink(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=30, db_index=True)
    campaign = models.ForeignKey(AffiliateCampaign, null=False, blank=False)

    def __unicode__(self):
        return "{0} for {1}".format(self.ip_address, self.campaign.token)

class AffiliateAdmin(admin.ModelAdmin):
    pass

class AffiliateCampaignAdmin(admin.ModelAdmin):
    pass

class AffiliateLinkAdmin(admin.ModelAdmin):
    pass

admin.site.register(Affiliate, AffiliateAdmin)
admin.site.register(AffiliateCampaign, AffiliateCampaignAdmin)
admin.site.register(AffiliateLink, AffiliateLinkAdmin)
