from django.shortcuts import render
from django.http import HttpResponse

from .models import MailVerify
import requests
import json

def verify(request):
	if request.method == 'POST':
		print request.body
		json.loads(request.body)
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
		


# Create more views here.
