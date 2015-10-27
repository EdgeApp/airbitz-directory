from restapi.locapi import reverseCountryMap
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, resolve
from django.template.defaultfilters import slugify
from airbitz import settings

import mailchimp
import logging
import phonenumbers

log=logging.getLogger("airbitz." + __name__)

def format_phone(number, country):
    try:
        c = reverseCountryMap(country)
        num = phonenumbers.parse(number, c)
        return phonenumbers.format_number(num,\
                phonenumbers.PhoneNumberFormat.INTERNATIONAL).replace(' ', '-')
    except:
        log.warn('Invalid number {0}:{1}'.format(number, country))
        return number


def mailchimp_list_signup(request, redirect_destination=None):
    if request.POST.get('signup_source', False): # try to get signup source from form else use url
        mc_source = request.POST.get('signup_source', 'unknown')
    else:
        mc_source = slugify(request.path_info)
        if mc_source == '':
            mc_source = 'home'

    mc_email = request.POST.get('email', '')
    mc_fname = request.POST.get('first', '')
    mc_lname = request.POST.get('last', '')

    mc_list_id = settings.MAILCHIMP_LIST_AIRBITZ_MAIN
    mc_list = mailchimp.utils.get_connection().get_list_by_id(mc_list_id)

    mc_merge_vars = {
        'SOURCE': mc_source,
        'FNAME': mc_fname,
        'LNAME': mc_lname
    }

    if redirect_destination is None:
        redirect_destination = resolve(request.path_info).url_name

    try:
        mc_list.subscribe(
            email_address=mc_email,
            double_optin=False,
            update_existing=True,
            merge_vars=mc_merge_vars
        )
        print 'SUBSCRIBED TO MAILCHIMP LIST:', mc_fname, mc_lname, mc_email, mc_source, redirect_destination
    except Exception as e:
        print 'MAILCHIMP SUBSCRIBE ERROR:', e


    return HttpResponseRedirect(reverse(redirect_destination))