#!/usr/bin/env python

import requests
import unittest

HOST='http://localhost:8000'
# HOST='http://admin.airbitz.co'
DEF_TOKEN='9962c7020d1ea099e81cfdc9a6c78485bd7c87e5'

SD_LL = '32.708727,-117.160679'
SF_LOC = 'San%20Francisco,%20CA,%20United%20States'

def get(path, payload=None, token=DEF_TOKEN):
    headers = {}
    if token:
        headers['Authorization'] = 'Token {0}'.format(token)
    if path.find('http') < 0:
        path = HOST + path
    return requests.get(path, headers=headers, verify=False)

def closeEnough(v1, v2):
    return float(v1) - float(v2) < 0.001

def isFeatured(biz):
    return any(c['name'] == 'Featured' for c in biz['categories'])

class TestApi(unittest.TestCase):

    def test_featured(self):
        print 'test_featured'
        r = get('/api/v1/search/?term=beer')
        self.assertEqual(r.status_code, 200)
        biz = r.json()['results'][0]
        self.assertTrue(isFeatured(biz))

    def test_search(self):
        print 'test_search'
        ll = '32.708727,-117.160679'
        r = get('/api/v1/search/?ll={0}'.format(ll))
        self.assertEqual(r.status_code, 200)

    def test_search_different_location(self):
        print 'test_search_different_location'
        r = get('/api/v1/search/?ll={0}&location={1}'.format(SD_LL, SF_LOC))
        self.assertEqual(r.status_code, 200)
        for b in r.json()['results']:
            if not isFeatured(b):
                n = r.json()['results'][1]
                self.assertEqual(n['city'], 'San Francisco')
                self.assertEqual(n['state'], 'CA')
                return;

    def test_pager(self):
        n = HOST + '/api/v1/search/?ll={0}&location={1}'.format(SD_LL, SF_LOC)
        bizMap = {}
        while n:
            print 'test_pager ', n
            r = get(n)
            self.assertEqual(r.status_code, 200)
            j = r.json()
            n = j['next']
            for r in j['results']:
                self.assertFalse(bizMap.has_key(r['bizId']))
                if not isFeatured(r):
                    bizMap[r['bizId']] = True

    def test_biz(self):
        print 'test_biz'
        ll = '32.708727, -117.160679'
        r = get('/api/v1/business/605/?ll={0}'.format(ll))
        self.assertEqual(r.status_code, 200)
        self.assertTrue(closeEnough(r.json()['distance'], 55515.66421306182))

if __name__ == '__main__':
    unittest.main()

