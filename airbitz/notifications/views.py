from django.db.models import Q
from rest_framework import authentication as auth
from rest_framework import generics
from rest_framework import permissions as perm
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

import logging

from notifications.models import Notification, HBitsPromos
from restapi.views import BetterTokenAuthentication

log=logging.getLogger("airbitz." + __name__)

DEFAULT_PAGE_SIZE=20

PERMS=(BetterTokenAuthentication, auth.SessionAuthentication,)
AUTH=(perm.IsAuthenticated, )
ADMIN_AUTH=(perm.DjangoModelPermissions, )

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


class HBitsPromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HBitsPromos
        fields = ('token',
                  'message',
                  'zero_message',
                  'tweet',
                  'claimed',
                  )

class HBitsClaimedPost(object):
    def __init__(self, claimed):
        self.claimed = claimed

class HBitsClaimedSeralizer(serializers.Serializer):
    claimed = serializers.BooleanField(required=True)

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.claimed = attrs.get('claimed', instance.claimed)
            return instance
        return HBitsClaimedPost(**attrs)

class HBitsPromoView(generics.RetrieveAPIView):
    serializer_class = HBitsPromoSerializer
    lookup_url_kwarg = 'token'
    authentication_classes = PERMS
    permission_classes = AUTH

    def get_queryset(self):
        return HBitsPromos.objects.filter(token=self.kwargs['token'])

    def retrieve(self, request, *args, **kwargs):
        try:
            self.object = self.get_queryset()[0]
        except:
            return Response(status=404, data={})
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)

class HBitsPromoList(generics.ListAPIView):
    serializer_class = HBitsPromoSerializer
    authentication_classes = PERMS
    permission_classes = AUTH
    paginate_by = 50
    paginate_by_param = 'page_size'

    def get_queryset(self):
        return HBitsPromos.objects.all()

class HBitsPromoClaimed(APIView):
    authentication_classes = PERMS
    permission_classes = AUTH
    post_serializer = HBitsClaimedSeralizer

    def post(self, request, *args, **kwargs):
        ser = self.post_serializer(data=request.DATA)
        if ser.is_valid():
            o = ser.object
            try:
                record = HBitsPromos.objects.get(token=self.kwargs['token'])
                record.claimed = o.claimed
                record.save()
                return Response(status=200, data={'detail': 'Record updated'})
            except Exception as e:
                print e
                return Response(status=404, data={'detail': 'Record does not exist'})
        else:
            return Response(status=500, data={'detail': 'Invalid input'})

class HBitsPromoCreate(APIView):
    authentication_classes = PERMS
    permission_classes = ADMIN_AUTH
    post_serializer = HBitsPromoSerializer

    queryset = HBitsPromos.objects.all()
    def post(self, request, *args, **kwargs):
        ser = self.post_serializer(data=request.DATA)
        if ser.is_valid():
            o = ser.object
            if HBitsPromos.objects.filter(token=o.token).exists():
                return Response(status=500, data={'detail': 'Record exists'})
            else:
                HBitsPromos.objects.create(token=o.token,
                                        message=o.message,
                                        zero_message=o.zero_message,
                                        tweet=o.tweet,
                                        claimed=False)
            return Response(status=201)
        else:
            return Response(status=500, data={'detail': 'Invalid input'})

