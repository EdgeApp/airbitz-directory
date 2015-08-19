from django.contrib import admin
from django.contrib.gis.db import models

import logging

logger = logging.getLogger(__name__)

class Notification(models.Model):
    ios_build_last = models.BigIntegerField(blank=True, null=True)
    ios_build_first = models.BigIntegerField(blank=True, null=True)

    android_build_last = models.BigIntegerField(blank=True, null=True)
    android_build_first = models.BigIntegerField(blank=True, null=True)

    title = models.CharField(max_length=255)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{0}".format(self.message)

class HBitsPromos(models.Model):
    class Meta:
        verbose_name = 'Hidden Bits Promo'
        verbose_name_plural = 'Hidden Bits Promos'

    token = models.CharField(unique=True, max_length=35)
    message = models.TextField(null=False)
    zero_message = models.TextField(null=False)
    tweet = models.TextField(null=False)
    claimed = models.BooleanField(default=False)

    def __unicode__(self):
        return "{0}".format(self.token)

