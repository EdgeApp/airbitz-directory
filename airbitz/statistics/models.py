from django.contrib.gis.db import models
from django.contrib import admin
import json

from actions import export_buysell_action

class Event(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    event_type = models.CharField(max_length=30)
    event_text = models.TextField(null=False)
    event_network = models.CharField(max_length=30)

    def btc(self):
        return self.j('btc')

    def partner(self):
        return self.j('partner')

    def user(self):
        return self.j('user')

    def j(self, k):
        try:
            return json.loads(self.event_text)[k]
        except:
            return ''

    def __unicode__(self):
        return "{0}".format(self.event_text)

class EventAdmin(admin.ModelAdmin):
    list_display = ('created',
                    'event_type',
                    'event_network',
                    'btc',
                    'partner',
                    'event_text',
                    )
    actions = [
        export_buysell_action()
    ]

admin.site.register(Event, EventAdmin)

