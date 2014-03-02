from restapi import api

def near(request):
    nearText = None
    if request.GET.get('near', None):
        nearText = request.GET.get('near', None)
    else:
        nearText = request.session.get('nearText', None) 
        if not nearText: 
            ip = api.getRequestIp(request)
            a = api.ApiProcess(ip=ip)
            nearText = a.suggestNearText()
    request.session['nearText'] = nearText
    return { 'near': nearText }

