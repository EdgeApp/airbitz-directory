from celery import task
from django.conf import settings

import logging
import requests
import urllib

log=logging.getLogger("restapi." + __name__)

DEF_CID=555

def ga_send(request, title):
    __ga_post__.delay(request.path, title, campaign=request.user.username, \
                      cid=request.META.get('HTTP_X_CLIENT_ID', DEF_CID),
                      useragent=request.META.get('HTTP_USER_AGENT', None),
                      ip=request.META.get('REMOTE_ADDR', None))

@task()
def __ga_post__(path, title, campaign=None, cid=None, ip=None, version=1,
                clientid=DEF_CID, useragent=None, hittype='pageview',
                domain='api.airbitz.co'):
    payload=dict(
        v=version,
        tid=settings.API_GOOGLE_ANALYTICS_PROPERTY_ID,
        cid=cid,
        cn=campaign,
        t=hittype,
        dh=domain,
        dp=urllib.quote_plus(path),
        dt=title)
    if ip:
        payload['uip'] = ip
    if useragent:
        payload['ua'] = useragent

    r = requests.post('https://ssl.google-analytics.com/collect', data=payload)
    # Should we do something if it fails?
    log.info('{0}: {1}'.format(r.status_code, payload))
