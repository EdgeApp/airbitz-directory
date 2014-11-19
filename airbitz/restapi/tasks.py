from celery import task
from django.conf import settings

import logging
import requests

log=logging.getLogger("restapi." + __name__)

def get_ip(request):
    try:
        return request.META['REMOTE_ADDR']
    except:
        return None

def ga_send(request, title):
    __ga_post__.delay(request.path, title, ip=get_ip(request))

@task()
def __ga_post__(path, title, ip=None, version=1,
                clientid=555, hittype='pageview',
                domain='api.airbitz.co'):
    payload=dict(
        v=version,
        tid=settings.API_GOOGLE_ANALYTICS_PROPERTY_ID,
        cid=clientid,
        t=hittype,
        dh=domain,
        dp=path,
        dt=title)
    if ip:
        payload['oip'] = ip
    r = requests.post('https://www.google-analytics.com/collect', data=payload)
    # Should we do something if it fails?
    log.info('{0}: {1}'.format(r.status_code, payload))
