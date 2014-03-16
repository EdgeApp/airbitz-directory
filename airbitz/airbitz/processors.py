from restapi import api
import logging

log=logging.getLogger()

def near(request):
    print request.META
    log.info(request.META)
    nearText = None
    if request.GET.has_key('location'):
        nearText = request.GET.get('location', None) or api.CURRENT_LOCATION
    else:
        nearText = request.session.get('nearText', None) 
        if not nearText: 
            ip = api.getRequestIp(request)
            a = api.ApiProcess(ip=ip)
            nearText = a.suggestNearText()
    request.session['nearText'] = nearText
    return { 'location': nearText }

