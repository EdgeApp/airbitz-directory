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