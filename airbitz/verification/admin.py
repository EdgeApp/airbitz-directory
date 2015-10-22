from django.contrib import admin
from .models import MailVerify

class MailVerifyAdmin(admin.ModelAdmin):
	fields = ['verify_id', 'verify_date', 'mail']
	list_display = ('verify_id', 'verify_date', 'mail')
	list_filter = ['verify_date']
	search_fields = ['verify_id', 'mail']

# Register your models here.
admin.site.register(MailVerify, MailVerifyAdmin)