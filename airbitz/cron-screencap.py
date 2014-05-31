import subprocess
import os
import datetime
from airbitz import settings
from directory.models import Business

'''
Makes screencapture image based on Airbitz Buisness ID
'''
def screencap(biz_id):
    casper_script = os.getcwd() + '/biz-screen-capture.js'
    casper_save = '--save=' + settings.MEDIA_ROOT + '/screencaps/'
    casper_url = '--url=' + settings.SCREENCAP_ABSOLUTE_URL
    casper_args = ' '.join(['casperjs', casper_script, casper_save, casper_url, str(biz_id)])
    print casper_args
    print subprocess.check_output(casper_args, shell=True)

'''
Queries for businesses published in the window given
'''
def get_biz_list(d1=datetime.date.today(), d2=None):
    b_list = []
    if not d2:
        pub = Business.objects.filter(status="PUB").filter(published__gte=d1)
    else:
        pub = Business.objects.filter(status="PUB").filter(published__gte=d1, published__lte=d2)
    for b in pub:
        b_list.append(b.id)
    b_list.sort(reverse=True)
    print b_list, '\n', 'BUSINESSES FOUND:', pub.count(), '\n'
    return b_list

'''
Makes screencapture images and consumes list of Airbitz business IDs that are published and live
'''
def get_screencaps(b_list=get_biz_list()):
    for id in b_list[:]:
        screencap(id)
        b_list.remove(id)
        print 'NEXT 5:', str(b_list[:5]), str(len(b_list)), 'LEFT'




date1 = datetime.date(2014, 5, 29)
date2 = date1 + datetime.timedelta(days=1)

get_biz_list()
biz_list.sort(reverse=True)

get_screencaps()