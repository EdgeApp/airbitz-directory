from restapi.api import suggestNearText

def near(request):
    if request.GET.get('near', None):
        nearText = request.GET.get('near', None)
        request.session['nearText'] = nearText
    else:
        nearText = request.session.get('nearText', None) 
        if not nearText: 
            nearText = suggestNearText(request.META['REMOTE_ADDR'])
            request.session['nearText'] = nearText
    return { 'near': nearText }

