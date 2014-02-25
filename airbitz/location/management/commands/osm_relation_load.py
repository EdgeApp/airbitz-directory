from django.core.management import BaseCommand
from django.contrib.gis.geos import Point

from location.models import OsmRelation

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(args[0]) as f:
            for line in f:
                values = line.split('\t')
                # Only load Admin and city, or villages
                if values[6] not in ('A', 'P'):
                    continue
                geo, created = GeoName.objects.get_or_create(
                    geonameid=values[0],
                )
                geo.name = values[1]
                geo.asciiname = values[2]
                geo.alternatenames = values[3]
                geo.center = Point(float(values[5]), float(values[4]))
                geo.feature_class = values[6]
                geo.feature_code = values[7]
                geo.country_code = values[8]
                geo.cc2 = values[9]
                geo.admin1_code = values[10]
                geo.admin2_code = values[11]
                geo.admin3_code = values[12]
                geo.admin4_code = values[13]
                # geo.population = values[14]
                # geo.elevation = values[15]
                # geo.dem = values[16]
                geo.timezone = values[17]
                geo.modification_date = values[18]
                geo.save()

