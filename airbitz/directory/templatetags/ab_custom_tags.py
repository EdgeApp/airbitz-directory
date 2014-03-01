from django import template
from django.template.defaultfilters import stringfilter
import re

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
        return "%d%%" % float(decimal * 100)
    except ValueError:
        return ''