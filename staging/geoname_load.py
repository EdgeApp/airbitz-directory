#!/usr/bin/env python
from __future__ import print_function
import pysolr
import sys

solr = pysolr.Solr('http://localhost:8983/solr/', timeout=100)
data = []
with open(sys.argv[1]) as f:
    for line in f:
        if len(data) == 10000:
            solr.add(data)
            data = []
        values = line.split('\t')
        postalcode=values[1]
        country=values[0]
        postalcode=values[1]
        place_name=values[2]
        admin_name1=values[3]
        admin_code1=values[4]
        admin_name2=values[5]
        admin_code2=values[6]
        admin_name3=values[7]
        lon,lat=float(values[10]), float(values[9])

        searchable=[]
        searchable.append("{0}, {1}".format(admin_name2, admin_code1))
        searchable.append("{0}, {1}".format(admin_name2, admin_name1))
        for s in searchable:
            data.append({
                "id": s,
                "postalcode": postalcode,
                "text": s,
                "content_auto": s,
                "admin1_code": admin_code1,
                "admin1_name": admin_name1,
                "admin2_code": admin_code2,
                "admin2_name": admin_name2,
                "admin3_name": admin_name3,
                "django_ct": "location.locationstring",
                "location": "{0},{1}".format(lat,lon)
            })

if len(data) > 0:
    solr.add(data)

solr.optimize()
