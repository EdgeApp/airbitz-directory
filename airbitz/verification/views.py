from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
# Non-Django stuff
from .models import MailVerify
import requests
import json
import datetime

def verify(request, verify_id):
	if request.method == 'POST':
		jRequest = json.loads(request.body)
		payload = {
		'secret': '6Le6_QsTAAAAABNk7sjeubFi38k-ElnYlv7Np8eu',
		'response': jRequest['g-recaptcha-response'], 
		'remoteip': request.META['REMOTE_ADDR']
		}
		r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
		if r.json()['success'] == True:
			v = MailVerify.objects.get(verify_id=verify_id) # Record that validation was successful
			v.verify_date = datetime.datetime.now()
			v.save()
			print "Successfully validated captcha for email: " + v.mail
			return HttpResponse(status=200) # Tell the client the captcha was successfully validated.
		else:
			print "Error validating Captcha token"
			return HttpResponse(status=401) # Tell the client there was an error validating.

	else:
		print ""
		return render(request, 'verification/index.html')
@csrf_exempt
def new(request): # Get request with json object of email and verification token.
	if request.method == 'POST':
		print request.body
		jRequest = json.loads(request.body)
		email = jRequest['email']
		verify_id = jRequest['verify_id']
		MailVerify(verify_id=verify_id, mail=email, verify_date=None).save();
		return HttpResponse("New verification added")
	else:
		return HttpResponse("Please send a POST request")
def since(request, verify_id):
	if verify_id == "all":
		print "All of them that have been verified"
		results = serializers.serialize("json", MailVerify.objects.filter(verify_date__lt=datetime.datetime.now()).order_by('verify_date'), fields=('verify_id'))
		return HttpResponse(results)
	else:
		sinceObj = get_object_or_404(MailVerify,verify_id=verify_id)
		sinceTime = sinceObj.verify_date
		print "Since Time: " + str(sinceTime)
		results = serializers.serialize("json", MailVerify.objects.filter(verify_date__gt=sinceTime).order_by('verify_date'), fields=('verify_id'))
		return HttpResponse(results)

# Create more views here.