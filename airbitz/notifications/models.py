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
    token = models.CharField(unique=True, max_length=35)
    message = models.TextField(null=False)
    zero_message = models.TextField(null=False)
    tweet = models.TextField(null=False)
    claimed = models.BooleanField(default=False)

    def __unicode__(self):
        return "{0}".format(self.token)

class NotificationAdmin(admin.ModelAdmin):
    pass

def format_string(obj, field):
    style = "overflow:hidden; white-space:nowrap; max-width:300px; text-overflow:ellipsis; -o-text-overflow:ellipsis;"
    return "<div style=\"{0}\">{1}</div>".format(style, (getattr(obj, field) or '').strip())

def format_message(obj):
    return format_string(obj, 'message')

def format_zero_message(obj):
    return format_string(obj, 'zero_message')

def format_tweet(obj):
    return format_string(obj, 'tweet')

format_message.allow_tags = True
format_message.admin_order_field = 'message'
format_zero_message.allow_tags = True
format_zero_message.admin_order_field = 'zero_message'
format_tweet.allow_tags = True
format_tweet.admin_order_field = 'tweet'

class HBitsPromosAdmin(admin.ModelAdmin):
    list_display = ('token', format_message, format_zero_message, format_tweet, )
    search_fields = ('token',)

admin.site.register(Notification, NotificationAdmin)
admin.site.register(HBitsPromos, HBitsPromosAdmin)
