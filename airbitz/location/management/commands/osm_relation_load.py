from django.db import connection
from django.contrib.gis.geos import GEOSGeometry
from django.core.management import BaseCommand

from location.models import OsmRelation, OsmBoundary

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def empty(s):
    if not s:
        return True
    if isinstance(s, str) and len(s.trim()) == 0:
        return True
    else:
        return False

class Command(BaseCommand):
    inserts = 0
    updates = 0
    skips = 0

    def handle(self, *args, **options):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT osm_id, admin_level, 
                pretty_name, country_code, 
                st_astext(centroid) 
            FROM carto_relation
            WHERE admin_level IS NOT NULL
              AND centroid IS NOT NULL
              AND name IS NOT NULL
        """)
        for row in cursor.fetchall():
            res = self.updateOrCreateRelation(row[0], row[1], \
                                              row[2], row[3], \
                                              row[4])
            if res:
                self.updateOrCreateArea(row[0])

        print "Inserts: ", self.inserts
        print "Updates: ", self.updates
        print "Skips: ", self.skips
            
    def updateOrCreateRelation(self, osm_id, admin_level, name, country_code, centroid):
        if empty(name) or empty(admin_level) or empty(centroid):
            self.skips = self.skips + 1
            return False
        c = GEOSGeometry(centroid, srid=900913)
        c.transform(4326)
        try:
            obj = OsmRelation.objects.get(osm_id=osm_id)
        except OsmRelation.DoesNotExist:
            obj = OsmRelation.objects.create(osm_id=osm_id, \
                                             admin_level=admin_level, \
                                             name=name, \
                                             country_code=country_code, \
                                             centroid=c)
            self.inserts = self.inserts + 1
        else:
            self.updates = self.updates + 1
            obj.admin_level = admin_level
            obj.name = name
            obj.country_code = country_code
            obj.centroid = c
            obj.save()
        return True


    def updateOrCreateArea(self, osm_id):
        cursor = connection.cursor()
        OsmBoundary.objects.filter(osm_id=osm_id).delete()
        cursor.execute("""
            SELECT st_astext(geom) 
            FROM carto_areas
            WHERE geom IS NOT NULL
              AND relation_id = %s
        """, [osm_id])
        for row in cursor.fetchall():
            geom = GEOSGeometry(row[0], srid=900913)
            geom.transform(4326)
            OsmBoundary.objects.create(osm_id=osm_id, geom=geom)

