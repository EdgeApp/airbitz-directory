from django.core.management import BaseCommand
from django.contrib.gis.geos import Point
import json

from directory.models import Business

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Command(BaseCommand):
    def handle(self, *args, **options):
        f = open(args[0])
        w = f.read()
        f.close()

        data = json.loads(w)
        for row in data:
            # Only Bitcoin, sorry Damian
            if row['type'] != 'node' and row['icon'] != 'bitcoin':
                continue
            title = None
            if row.has_key('title'):
                title = row['title']
            center = Point((row['lon'], row['lat']))
            if not title:
                continue
            print title,
            biz, created = Business.objects.get_or_create(name=title, center=center)
            if created:
                print "...created\r"
            else:
                print "...updating\r"
            if row.has_key('desc') and not biz.description:
                biz.description = row['desc']
            if row.has_key('web') and not biz.website:
                biz.website = row['web']
            if row.has_key('addr') and not biz.address:
                biz.address = row['addr']
            if row.has_key('city') and not biz.admin3_name:
                biz.admin3_name = row['city']
            if row.has_key('country') and not biz.country:
                biz.country = row['country']
            if row.has_key('phone') and not biz.phone:
                biz.phone = row['phone']
            biz.save()
            
