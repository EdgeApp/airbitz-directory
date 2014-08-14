from django.core.management import BaseCommand

from directory.models import Business
from airbitz import regions_data

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Command(BaseCommand):
    def handle(self, *args, **options):
        # printing variables
        dashes = "------------------------------------"

        active_countries_list = regions_data.get_active_country_codes()

        # base query
        q = Business.objects.filter(status="PUB", country__in=active_countries_list)

        # admin1_code sanity queries
        q_spaces =      q.filter(admin1_code__regex="\s+$")
        q_length =      q.filter(admin1_code__regex="^[a-z][A-Z]{0,5}$")
        q_char =        q.exclude(country="AU").filter(admin1_code__regex=".{3,30}$").values('admin1_code').count()

        # output
        print dashes
        print "*** ISSUES WITH SPACES ****"
        for i in q_spaces:
            print i.name, i.admin1_code

        print dashes
