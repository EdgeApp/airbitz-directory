from django.contrib import admin

# Register your models here.
from notifications.models import Notification, HBitsPromos


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('modified',
                    'android_build_last',
                    'ios_build_last',
                    'title',
                    '_get_message',
                    )

    def _get_message(self, obj):
        return u'%s' % obj.message

    _get_message.allow_tags = True



admin.site.unregister(Notification)

admin.site.register(Notification, NotificationAdmin)