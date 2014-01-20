# -*- coding: utf-8 -*-

# I ran into a certificate error. This SO fixed the problem.
# http://stackoverflow.com/questions/13321302/python-foursquare-ssl3-certificate-verify-failed
from django.contrib.gis.geos import Point
from datetime import datetime
import foursquare
import logging

from directory.models import BusinessImage, BusinessHours
from airbitz.settings import FS_CLIENT_ID, FS_CLIENT_SECRET

log=logging.getLogger("airbitz." + __name__)

def parseTime(t):
    if t == None:
        return None
    try:
        if t == 'Midnight':
            return datetime.strptime('12:00 AM', '%I:%M %p')
        elif t == 'Noon':
            return datetime.strptime('12:00 PM', '%I:%M %p')
        else:
            return datetime.strptime(t, '%I:%M %p')
    except Exception as e:
        log.error(e)
        return None

def fsformatDay(d):
    if d == 'Sun': return 0
    elif d == 'Mon': return 1
    elif d == 'Tue': return 2
    elif d == 'Wed': return 3
    elif d == 'Thu': return 4
    elif d == 'Fri': return 5
    elif d == 'Sat': return 6
    elif d == 'Today': 
        d = datetime.now()
        return d.weekday() + 1
    raise "Can't match %s" % d


def bcformatDay(d):
    if d == 0: return 'sunday'
    elif d == 1: return 'monday'
    elif d == 2: return 'tuesday'
    elif d == 3: return 'wednesday'
    elif d == 4: return 'thursday'
    elif d == 5: return 'friday'
    elif d == 6: return 'saturday'
    raise "Can't match %s" % d


def splitTime(s):
    q = u"–"
    if s.find(q):
        arr = s.split(q)
        o = parseTime(arr[0])
        if len(arr) > 1:
            c = parseTime(arr[1])
        else:
            c = None
    else:
        o = parseTime(s)
        c = None
    return (o, c)

def splitTimes(hours):
    times = []
    for r in hours:
        times += [splitTime(r['renderedTime'])]
    return times

def splitDays(s):
    q = u"–"
    ds = []
    arr = s.split(',')
    for g in arr:
        r = g.split(q)
        s = fsformatDay(r[0])
        if len(r) > 1:
            e = fsformatDay(r[1])
            ds += range(s, e + 1)
        else:
            ds += [s]
    return ds


def parseTimeframes(timeframes):
    acc = []
    for frame in timeframes:
        days = splitDays(frame['days'])
        times = splitTimes(frame['open'])
        for d in days:
            for (o, c) in times:
                hours = {}
                hours['day'] = bcformatDay(d)
                hours['open'] = o.time()
                hours['close'] = c.time()
                acc.append(hours)
    return acc

class FoursquareClient:
    def __init__(self):
        self.client = foursquare.Foursquare(client_id=FS_CLIENT_ID,\
                                            client_secret=FS_CLIENT_SECRET)

    def update_business(self, biz, fsId):
        fq_data = self.client.venues(fsId)
        data = fq_data['venue']
        loc = data['location']
        con = data['contact']
        biz.name = data.get('name', '')
        biz.website = data.get('url', '')
        biz.description = data.get('decription', '')
        biz.phone = con.get('phone', '')
        biz.website = data.get('url', '')
        biz.center = Point(float(loc.get('lng', 1.0)),\
                           float(loc.get('lat', 1.0)))
        biz.address = loc.get('address', '')
        biz.postalcode = loc.get('postalCode', '')
        biz.city = loc.get('city', '')
        biz.state = loc.get('state', '')
        biz.country = loc.get('country', '')

        try:
            images = []
            img_groups = fq_data['venue']['photos']['groups']
            for grp in img_groups:
                for img in grp['items']:
                    images.append(img)
            images.sort(key=lambda img:(img['width']), reverse=True)
            if len(images) > 0: 
                for i in images:
                    img_url = "%s%sx%s%s" % (i['prefix'], i['width'], i['height'], i['suffix'])
                    img = BusinessImage.create_from_url(biz.id, img_url)
                    if img and not biz.landing_image:
                        biz.splash_image = img
        except (IndexError, KeyError) as e:
            log.error("Error while getting images for biz w/ Foursquare ID %s" % biz.foursquare_id)
            log.exception(e)
        biz.save()

        if data.has_key('hours'):
            self.parse_hours(biz, data['hours']['timeframes'])
        else:
            log.warn('no hours')

        return True

    def parse_hours(self, place, hours):
        try:
            self.save_times('hours', place, hours)
        except Exception as e:
            log.error(e)

    def save_times(self, time_type, biz, data):
        results = parseTimeframes(data)
        for r in results:
             if not BusinessHours.objects.filter(business=biz, dayOfWeek=r['day'], hourStart=r['open'], hourEnd=r['close']).exists():
                 BusinessHours.objects.create(business=biz, dayOfWeek=r['day'], hourStart=r['open'], hourEnd=r['close'])


