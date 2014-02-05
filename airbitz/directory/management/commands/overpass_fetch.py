from django.core.management import BaseCommand
from django.contrib.gis.geos import Point
import json

from directory.models import Business, SocialId

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
            if row['type'] != 'node' and row['type'] != 'way':
                continue
            title = None
            if row.has_key('title'):
                title = row['title']
            if not title:
                continue
            center = Point((row['lon'], row['lat']))
            try:
                sid = SocialId.objects.get(social_type='osm', social_id=row['id'])
                biz = sid.business
                created = False
            except SocialId.DoesNotExist:
                biz = Business.objects.create(name=title, center=center)
                sid = SocialId.objects.create(social_type='osm', social_id=row['id'], business=biz)
                created = True

            print title,
            if created:
                print "...created"
            else:
                if biz.status in ( 'PUB', 'PEN' ):
                    print "...skipping"
                    continue
                else:
                    print "...updating"
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
