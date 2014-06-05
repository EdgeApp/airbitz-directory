import os
import sys
import subprocess32 as subprocess
import urllib2
import json
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airbitz.settings')
from airbitz import settings
from directory.models import Business

'''
Makes screencapture image based on Airbitz Buisness ID
REQUIREMENTS: casperjs & phantomjs binaries must be in path for execution
'''
def screencap(biz_id):
    casper_timeout = 30
    casper_path = '/home/' + settings.SYS_USER + '/local/bin/casperjs'
    try:
        casper_script = os.path.dirname(os.path.dirname(__file__)) + '/airbitz/biz-screen-capture.js'
    except NameError as e:
        print 'NOT RUNNING FROM FILE'
        casper_script = '/home/vagrant/airbitz/ENV/airbitz/biz-screen-capture.js'
    casper_save = '--save=' + settings.MEDIA_ROOT + '/screencaps/'
    casper_url = '--url=' + settings.SCREENCAP_ABSOLUTE_URL
    casper_args = ' '.join([casper_path, casper_script, casper_save, casper_url, str(biz_id)])
    print 'CASPER CMD:', casper_args

    try:
        print subprocess.check_output(casper_args, shell=True, timeout=casper_timeout)
    except subprocess.TimeoutExpired:
        print '**** CASPERJS TIME IS UP GOTTA MOVE ON ****'
    except subprocess.CalledProcessError as e:
        print '*** CASPER CMD ERROR CODE = ', e.returncode

def query_biz_list(d1=datetime.date.today(), d2=None):
    b_list = []
    if not d2:
        pub = Business.objects.filter(status="PUB").filter(modified__gte=d1)
    else:
        pub = Business.objects.filter(status="PUB").filter(modified__lte=d1, modified__gte=d2)
    for b in pub:
        b_list.append(b.id)
    b_list.sort(reverse=True)
    print b_list, '\n', 'BUSINESSES MODIFIED :', pub.count(), '\n'

'''
Queries for businesses modified in the window given otherwise it will just query anything modified today
'''
def get_biz_list():
    url = 'https://airbitz.co/mgmt/api/biz/caplist'
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    b_list = []
    for result in data['results']:
        print result['id']
        b_list.append(result['id'])

    print b_list, '\n', 'BUSINESSES MODIFIED :', len(b_list), '\n'
    return b_list

'''
Makes screencapture images and consumes list of Airbitz business IDs that are modified and live
'''
def get_screencaps(b_list=get_biz_list()):
    for bId in b_list[:]:
        screencap(bId)
        b_list.remove(bId)
        print 'NEXT 5:', str(b_list[:5]), str(len(b_list)), 'LEFT'


# interval = datetime.timedelta(minutes=15)
# date1 = datetime.datetime.today()
# date2 = date1 - interval
#
# biz_list = query_biz_list(date1, date2)


biz_list = get_biz_list()
biz_list.sort(reverse=True)

'''
Check if argument was passed from CMD line
'''
if len(sys.argv) < 2:
    get_screencaps(biz_list)
else:
    get_screencaps(sys.argv[1:])