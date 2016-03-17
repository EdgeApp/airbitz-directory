from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from pybitid import bitid
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response 
from rest_framework.views import APIView

from models import Affiliate, AffiliateCampaign, CampaignVariable, AffiliateLink
from restapi.views import AUTH, PERMS 

import pytz
import random
import string

def statusResponse(httpcode=status.HTTP_200_OK, data=None):
    return Response(status=httpcode, data=data)

def errUnauthorized(data=None):
    return statusResponse(status.HTTP_401_UNAUTHORIZED, data=data)

def errInvalidRequest(data=None):
    return statusResponse(status.HTTP_400_BAD_REQUEST, data=data)

class RegistrationFormObject(object):
    def __init__(self, bitid_address=None, bitid_signature=None, bitid_url=None, payment_address=None):
        self.bitid_address=bitid_address
        self.bitid_signature=bitid_signature
        self.bitid_url=bitid_url
        self.payment_address=payment_address

class RegistrationFormSerializer(serializers.Serializer):
    bitid_address=serializers.CharField(required=True)
    bitid_signature=serializers.CharField(required=False)
    bitid_url=serializers.CharField(required=False)
    payment_address=serializers.CharField(required=True)

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.bitid_address = attrs.get('bitid_address', instance.bitid_address)
            instance.bitid_signature = attrs.get('bitid_signature', instance.bitid_signature)
            instance.bitid_url = attrs.get('bitid_url', instance.bitid_url)
            instance.payment_address = attrs.get('payment_address', instance.payment_address)
            return instance
        return RegistrationFormObject(**attrs)

def check_signature(affiliate):
    if affiliate.bitid_signature:
        return bitid.signature_valid(affiliate.bitid_address, affiliate.bitid_signature, affiliate.bitid_url, affiliate.bitid_url)
    else:
        return bitid.address_valid(affiliate.bitid_address)

def random_token():
    valid_token = False
    while not valid_token:
        try:
            token = ''.join([random.choice(string.digits + string.letters) for i in range(0, 3)])
            AffiliateCampaign.objects.get(token=token)
        except AffiliateCampaign.DoesNotExist:
            valid_token = True
    return token

class RegistrationView(APIView):
    post_serializer = RegistrationFormSerializer
    authentication_classes = PERMS
    permission_classes = AUTH

    def get(self, request):
        uri = request.build_absolute_uri()
        nonce = bitid.generate_nonce()
        bitid_uri = bitid.build_uri(uri, nonce)
        return statusResponse(data={
            'bitid_uri': bitid_uri
        })

    def post(self, request):
        ser = self.post_serializer(data=request.DATA)
        if ser.is_valid():
            if not check_signature(ser.object):
                return errUnauthorized(data={
                    "error": "Invalid signature"
                })
            else:
                (affiliate, _) = Affiliate.objects.get_or_create(
                                    bitid_address=ser.object.bitid_address)
                (campaign, created) = AffiliateCampaign.objects.get_or_create(
                                        affiliate=affiliate,
                                        payment_address=ser.object.payment_address)
                if created:
                    campaign.token = random_token()
                    campaign.save()
                    # We do this by default, remove later
                    CampaignVariable.objects.get_or_create(
                        campaign=campaign,
                        key='gift_card_affiliate_fee',
                        key_type='percent',
                        value='20')
            uri = request.build_absolute_uri()
            affiliate_link = request.build_absolute_uri(reverse('affiliate_touch_short', args=(campaign.token, )))
            if uri.find('airbitz.co') > -1:
                affiliate_link = 'https://airbitz.co' + reverse('affiliate_touch_short', args=(campaign.token, ))
            return statusResponse(data={
                'affiliate_link': affiliate_link
            })
        else:
            return errInvalidRequest(data={
                "error": "Invalid POST variables" 
            })

def touch(request, token):
    try:
        ip_address = request.META.get('REMOTE_ADDR')
        campaign = AffiliateCampaign.objects.filter(token=token).last()
        if campaign:
            AffiliateLink.objects.get_or_create(campaign=campaign, ip_address=ip_address)
    except Exception as e:
        print e

    ua = request.META.get('HTTP_USER_AGENT', '').lower()
    if ua.find('android') > -1 or ua.find('linux') > -1:
        url = 'https://play.google.com/store/apps/details?id=com.airbitz'
    else:
        url = 'https://itunes.apple.com/us/app/bitcoin-wallet-airbitz/id843536046?mt=8'
    return HttpResponseRedirect(url)

EXPIRED_MINUTES = 10

class QueryView(APIView):
    authentication_classes = PERMS
    permission_classes = AUTH

    def get(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        print ip_address
        try:
            expired = datetime.now(pytz.utc) - timedelta(minutes=EXPIRED_MINUTES)
            link = AffiliateLink.objects.get(ip_address=ip_address, created__gte=expired)
            variables = [{
                'key': c.key,
                'key_type': c.key_type,
                'value': c.value
            } for c in CampaignVariable.objects.filter(campaign=link.campaign).order_by('key')] 
            return statusResponse(data={
                'expires': (link.created + timedelta(minutes=EXPIRED_MINUTES)),
                'affiliate_address': link.campaign.payment_address,
                'objects': variables
            })
        except AffiliateLink.DoesNotExist as e:
            print e
        return errInvalidRequest(data={
            "error": "No matching device"
        })
