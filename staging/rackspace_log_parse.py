import os
import re
import zipfile
import csv

# Creates csv file from individual rackspace zips of logs
# accessed_url, src_ip, date, http_request, user_agent

# get screenshot files list
logs_path = '/staging/rackspace/logs/'
zip_files = []
log_files = []
csv_file_rows = []
csv_filename = 'access_log'
log_to_csv_pattern = '^.*\d+_\d+ (.*\.*) (\d+\.\d+\.\d+\.\d+) .*\[(.*?)\].*?\"(.*?)\".*?\".*?\".*?\"(.*?)\".*'


log_dir_files = os.listdir(logs_path)
# get list of files for unzip
for filename in log_dir_files:
    zip_match = re.findall(r'.*\.zip$', filename)
    try:
        zip_files.append(zip_match[0])
    except IndexError as e:
        pass

# unzip zip files in dir
for zf in zip_files:
    zfile = zipfile.ZipFile(logs_path + zf)
    for name in zfile.namelist():
        (dirname, filename) = os.path.split(name)
        print "Decompressing " + filename + " on " + logs_path
        if not os.path.exists(logs_path):
            os.makedirs(logs_path)
        zfile.extract(filename, logs_path + dirname)


log_dir_files = os.listdir(logs_path)
# get list of access_log files
for filename in log_dir_files:
    log_match = re.findall(r'access_log_.*', filename)
    try:
        log_files.append(log_match[0])
    except IndexError as e:
        pass

log_files.sort()


# open log files and parse each line then add matches to the csv_file_rows list
total_files = len(log_files)
i = 0
for log_file in log_files:
    i += 1
    print 'PARSING', log_file, i, 'of', total_files
    with open(logs_path + log_file) as f:
        for line in f:
            matches = re.match(log_to_csv_pattern, line)
            if matches:
                csv_file_rows.append(matches.groups())


# Take csv_files_rows list and create csv file from it
with open(logs_path + csv_filename + '.csv', 'wb') as result:
    print '\nWRITING TO', logs_path + csv_filename
    writer = csv.writer(result, dialect='excel')
    writer.writerows(csv_file_rows)
