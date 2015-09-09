from django.db import models

from django.contrib import admin

class MailVerify(models.Model):
	verify_id = models.CharField(max_length=255)
	verify_date = models.DateTimeField(null=True)
	mail = models.EmailField(max_length=255)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

admin.site.register(MailVerify)
# Create your models here.
