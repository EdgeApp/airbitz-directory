from restapi.api import suggestNearByRequest

def near(request):
    nearText = None
    if request.GET.get('near', None):
        nearText = request.GET.get('near', None)
    else:
        nearText = request.session.get('nearText', None) 
        if not nearText: 
            nearText = suggestNearByRequest(request)
    request.session['nearText'] = nearText
    return { 'near': nearText }

