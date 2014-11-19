from rest_framework import authentication as auth
from rest_framework import generics
from rest_framework import permissions as perm
from rest_framework import serializers

import logging

from notifications.models import Notification
from restapi.views import BetterTokenAuthentication

log=logging.getLogger("airbitz." + __name__)

DEFAULT_PAGE_SIZE=20

PERMS=(BetterTokenAuthentication, auth.SessionAuthentication,)
AUTH=(perm.IsAuthenticated, )

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id',
                  'ios_build',
                  'android_build',
                  'title',
                  'message',
                  )

class NotificationView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    authentication_classes = PERMS
    permission_classes = AUTH

    def get_queryset(self):
        since_id = self.request.QUERY_PARAMS.get('since_id', 0)
        ios_build = self.request.QUERY_PARAMS.get('ios_build', None)
        android_build = self.request.QUERY_PARAMS.get('android_build', None)

        kwargs=dict()
        kwargs['id__gt']=since_id
        if ios_build:
            kwargs['ios_build__gte']=int(ios_build)
        if android_build:
            kwargs['android_build__gte']=int(android_build)

        return Notification.objects.filter(**kwargs).order_by('id')

