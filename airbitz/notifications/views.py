from django.db.models import Q
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

        q = Q(id__gt=since_id)
        if ios_build:
            # ios_build_first <= ios_build <= ios_build_last
            q = q & Q(ios_build_last__gte=int(ios_build))
            q = q & (Q(ios_build_first__isnull=True) | Q(ios_build_first__lte=ios_build))
        if android_build:
            # android_build_first <= android_build <= android_build_last
            q = q & Q(android_build_last__gte=int(android_build))
            q = q & (Q(android_build_first__isnull=True) | Q(android_build_first__lte=android_build))
        if not android_build and not ios_build:
            q = q & Q(android_build_last__isnull=True) & Q(ios_build_last__isnull=True)

        return Notification.objects.filter(q).order_by('id')

