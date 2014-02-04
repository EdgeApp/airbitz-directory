from django.core.management import BaseCommand
from django.contrib.gis.geos import Point

from location.models import LocationString, GeoNameZip

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(args[0]) as f:
            for line in f:
                values = line.split('\t')
                geo, created = GeoNameZip.objects.get_or_create(postalcode=values[1])
                geo.country=values[0]
                geo.postalcode=values[1]
                geo.place_name=values[2]
                geo.admin_name1=values[3]
                geo.admin_code1=values[4]
                geo.admin_name2=values[5]
                geo.admin_code2=values[6]
                geo.admin_name3=values[7]
                geo.center = Point(float(values[10]), float(values[9]))
                geo.save()

                s0 = "{0}".format(values[3])
                self.update(values, s0, admin2=False, admin3=False, postalcode=False)
                s1 = "{0}, {1}".format(values[5], values[3])
                self.update(values, s1, admin3=False)
                s2 = "{0}, {1}".format(values[5], values[4])
                self.update(values, s2, admin3=False)
                s3 = "{0}, {1}".format(values[2], values[4])
                self.update(values, s3, admin3=False)
                s4 = "{0}, {1}".format(values[2], values[3])
                self.update(values, s4, place_name=True, admin3=False)

    def update(self, values, id, place_name=False, admin1=True, \
                                 admin2=True, admin3=True, postalcode=True):
        geo, created = LocationString.objects.get_or_create(content_auto=id)
        if postalcode:
            geo.postalcode=values[1]
        if admin1:
            geo.admin1_name=values[3]
            geo.admin1_code=values[4]
        if admin2:
            geo.admin2_name=values[5]
            geo.admin2_code=values[6]
        if admin3:
            geo.admin3_name=values[7]
        elif place_name:
            geo.admin3_name=values[2]
        geo.center = Point(float(values[10]), float(values[9]))
        geo.save()
