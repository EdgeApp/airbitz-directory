from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse

from .models import MailVerify
import requests
import json

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
			print "Successfully validated captcha"
			return HttpResponse(status=200) # Tell the client the captcha was successfully validated.
			#record that validation was successful
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

# Create more views here.