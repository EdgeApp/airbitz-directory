from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from restapi.views import PERMS, AUTH
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
            return Response(status=200, data={'detail': 'Event created'})
        else:
            return Response(status=500, data={'detail': 'Invalid input'})
