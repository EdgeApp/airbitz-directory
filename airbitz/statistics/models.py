from django.contrib.gis.db import models
from django.contrib import admin

class Event(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    event_type = models.CharField(max_length=30)
    event_text = models.TextField(null=False)
    event_network = models.CharField(max_length=30)

    def __unicode__(self):
        return "{0}".format(self.event_text)

class EventAdmin(admin.ModelAdmin):
    list_display = ('created',
                    'event_type',
                    'event_network',
                    'event_text',
                    )

admin.site.register(Event, EventAdmin)
