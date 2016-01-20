from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
import json

from restapi.views import PERMS, AUTH
from restapi.tasks import send_purchase
from statistics.models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('event_type', 'event_text', 'event_network',)

class EventView(APIView):
    authentication_classes = PERMS
    permission_classes = AUTH
    post_serializer = EventSerializer

    def post(self, request, *args, **kwargs):
        ser = self.post_serializer(data=request.DATA)
        if ser.is_valid():
            o = ser.object
            record = Event.objects.create(event_type=o.event_type,\
                                          event_network=o.event_network,\
                                          event_text=o.event_text)
            record.save()

            if o.event_type in ['purchase', 'refund', 'sell', 'buy', ]:
                try:
                    j = json.loads(o.event_text)
                    btc = j['btc']
                    partner = j['partner']
                    send_purchase(btc, partner, o.event_type, o.event_network)
                except Exception as e:
                    print 'Bad json, skip ', e
            return Response(status=200, data={'detail': 'Event created'})
        else:
            return Response(status=500, data={'detail': 'Invalid input'})
