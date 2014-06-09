import os
import re
import csv


june_log_file = '/staging/rackspace/logs/access_log_june.csv'
may_log_file = '/staging/rackspace/logs/access_log_may.csv'

pattern_biz_view = 'api.airbitz.*api/v1/business/\d+ .*'
pattern_biz_search = 'api.airbitz.*api/v1/search/.*'

list_biz_views = []
list_biz_searches = []

log_file = june_log_file

with open(log_file, 'rb') as csvfile:
    log = csv.reader(csvfile)

    for row in log:
        row = ''.join(row) # row is a list we need it a string
        match_biz_search = re.match(pattern_biz_search, row)
        match_biz_view = re.match(pattern_biz_view, row)

        if match_biz_search is not None:
            list_biz_searches.append(match_biz_search)

        if match_biz_view is not None:
            list_biz_views.append(match_biz_view)


print '----------------------------'
print log_file
print '----------------------------'
print 'SEARCHES:', len(list_biz_searches)
print 'BUSINESS VIEWS:', len(list_biz_views)
print '----------------------------'