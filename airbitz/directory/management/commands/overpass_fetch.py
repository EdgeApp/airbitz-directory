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
            print title, row['id']
            try:
                sid = SocialId.objects.get(social_type='osm', social_id=row['id'])
                biz = sid.business
                created = False
            except SocialId.MultipleObjectsReturned:
                print 'Multiple entries!'
                continue
            except SocialId.DoesNotExist:
                biz = Business.objects.create(status='DR', name=title, center=center)
                sid = SocialId.objects.create(social_type='osm', social_id=row['id'], business=biz)
                created = True

            if created:
                print "...created"
            else:
                if biz.status in ( 'PUB', 'PEN' ):
                    print "...skipping"
                    continue
                else:
                    print "...updating"
            if row.has_key('desc'):
                biz.description = row['desc']
            if row.has_key('web'):
                biz.website = row['web']
            if row.has_key('addr'):
                biz.address = row['addr']
            if row.has_key('city'):
                biz.admin3_name = row['city']
            if row.has_key('country'):
                biz.country = row['country']
            if row.has_key('phone'):
                biz.phone = row['phone']
            biz.save()
