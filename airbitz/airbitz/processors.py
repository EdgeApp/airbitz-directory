
from restapi.views import buildNearText

def near(request):
    nearText = request.session.get('nearText', None) 
    print nearText
    if not nearText: 
        nearText = buildNearText(request.META['REMOTE_ADDR'])
        print request.META['REMOTE_ADDR'], nearText
        request.session['nearText'] = nearText
    return { 'near': nearText }

