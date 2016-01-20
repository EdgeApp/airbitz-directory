from celery import task
from django.conf import settings

import logging
import requests
import urllib
import time

log=logging.getLogger("restapi." + __name__)

DEF_CID=555

def ga_send(request, title):
    timestamp = int(time.time())
    __ga_post__.delay(request.path, title, campaign=request.user.username, \
                      cid=request.META.get('HTTP_X_CLIENT_ID', DEF_CID),
                      useragent=request.META.get('HTTP_USER_AGENT', None),
                      ip=request.META.get('REMOTE_ADDR', None), timestamp=timestamp)

@task()
def __ga_post__(path, title, campaign=None, cid=None, ip=None, version=1,
                clientid=DEF_CID, useragent=None, hittype='pageview',
                domain='api.airbitz.co', timestamp=None):
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

    payload=dict(
        idsite=settings.API_PIWIK_SITE_ID,
        token_auth=settings.API_PIWIK_TOKEN,
        action_name=title,
        send_image=0,
        uid=cid,
        rec=1,
        cdt=timestamp,
        url=urllib.quote_plus('https://' + domain + '/' + path)
    )
    if ip:
        payload['cip'] = ip
    if useragent:
        payload['ua'] = useragent
    r = requests.post('https://analytics.it.airbitz.co/analytics/piwik/piwik.php', data=payload)
    log.info('{0}: {1}'.format(r.status_code, payload))
