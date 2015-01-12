from restapi.locapi import reverseCountryMap

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
