from django import template
from django.template.defaultfilters import stringfilter
import re
from directory import utils

register = template.Library()




# Simple find and replace via regex
# https://djangosnippets.org/snippets/60/
#
@register.filter
@stringfilter
def replace ( string, args ):
    search  = args.split(args[0])[1]
    replace = args.split(args[0])[2]

    return re.sub( search, replace, string )


# Simple conversion from decimal to percentage
#
@register.filter(name='decimal_to_percent')
def decimal_to_percent(decimal):
    try:
        if str(decimal)[4] == '0':
            return "%d%%" % float(decimal * 100)
        else:
            return "%.1f%%" % float(decimal * 100)

    except ValueError:
        return ''

# Format phone number
@register.filter(name='format_phone')
def format_phone(number, country):
    return utils.format_phone(number, country)
