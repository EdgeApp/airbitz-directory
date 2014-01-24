from django.core.management import BaseCommand
from django.contrib.gis.geos import Point

from directory.models import GeoNameZip

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(args[0]) as f:
            for line in f:
                values = line.split('\t')
                geo, created = GeoNameZip.objects.get_or_create(
                    country=values[0],
                    postalcode=values[1],
                    place_name=values[2],
                    admin_name1=values[3],
                    admin_code1=values[4],
                    admin_name2=values[5],
                    admin_code2=values[6],
                    admin_name3=values[7],
                    center = Point(float(values[10]), float(values[9]))
                )
