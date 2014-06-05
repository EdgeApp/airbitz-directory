import os
import re
from directory.models import Business


b_list = []
ss_list = []

# get currently published businesses
pub = Business.objects.filter(status="PUB")
for b in pub:
    b_list.append(b.id)


# get screenshot files list
ss_path = '/home/bitz/media/screencaps'
ss_files = os.listdir(ss_path)

for filename in ss_files:
    match = re.findall(r'\d+', filename)
    try:
        ss_list.append(int(match[0]))
    except IndexError as e:
        print e


# find out how many published businesses don't have screenshots
need_ss = list(set(b_list) - set(ss_list))
need_ss.sort()

published_count = len(b_list)
screencap_count = len(ss_list)

print '-------------------------------'
print 'PUBLISHED IN DB:', published_count
print 'SCREENCAPS ON DISK:', screencap_count
print 'SCREENSHOTS MISSING', published_count - screencap_count
print '-------------------------------'
print ''
print need_ss