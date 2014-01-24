from restapi.api import suggestNearText

def near(request):
    nearText = request.session.get('nearText', None) 
    print nearText
    if not nearText: 
        nearText = suggestNearText(request.META['REMOTE_ADDR'])
        request.session['nearText'] = nearText
    return { 'near': nearText }

