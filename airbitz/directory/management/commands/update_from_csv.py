from django.core.management import BaseCommand
from django.utils.dateparse import parse_date
from directory.models import Business
import csv
import random

from messytables import CSVTableSet, type_guess, \
  types_processor, headers_guess, headers_processor, \
  offset_processor, any_tableset

# HARDCODED COLUMN DEFINITIONS
# FOR https://docs.google.com/spreadsheets/d/1kBWmSpTJ2hYBNnAEbC5ggKWRENxlch-cI_H6zSED0BE/edit#gid=0
ID=18
PUBLISHED=1
UPDATE=2
NAME=3
WEBSITE=4
PHONE=5
STREET_ADDRESS=6
CITY=7
EMAIL_PRIMARY=8
EXTRA=9

O_NAME=10


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **options):
        # hardcoded file name temporarily
        fh = open('biz.csv', 'rb')

        table_set = CSVTableSet(fh) # Load a file object:

        # If you aren't sure what kind of file it is, you can use
        # any_tableset.
        #table_set = any_tableset(fh)

        # A table set is a collection of tables:
        row_set = table_set.tables[0]

        # A row set is an iterator over the table, but it can only
        # be run once. To peek, a sample is provided:

        print row_set.sample.next()

        # guess header names and the offset of the header:
        offset, headers = headers_guess(row_set.sample)
        row_set.register_processor(headers_processor(headers))

        # add one to begin with content, not the header:
        row_set.register_processor(offset_processor(offset + 1))

        # guess column types:
        types = type_guess(row_set.sample, strict=True)

        # and tell the row set to apply these types to
        # each row when traversing the iterator:
        row_set.register_processor(types_processor(types))

        # now run some operation on the data:
        for row in row_set:
            id = row[ID].value
            published = row[PUBLISHED].value
            update = row[UPDATE].value
            name = row[NAME].value
            website = row[WEBSITE].value
            phone = row[PHONE].value
            street_address = row[STREET_ADDRESS].value
            city = row[CITY].value
            email_primary = row[EMAIL_PRIMARY].value
            extra = row[EXTRA].value

            o_name = row[O_NAME].value

            # for cell in row:
            #     print cell.value
            website = '' if website == 'http://' else website

            print ''
            print '****** airbitz.co/biz/' + str(id) + '/ **************************'

            if update == '1':
                print '-- UPDATE: ' + o_name + ' [' + update + ']'
                biz = Business.objects.get(pk=id)

                if biz:
                    print 'UPDATE: [' + str(update) + ']', id, o_name
                    print 'ORIG:', biz

                    if not name == '':
                        print 'UPDATE NAME:', name
                        biz.name = name
                    if not website == '':
                        print 'UPDATE WEBSITE:', website
                        biz.website = website
                    if not phone == '':
                        print 'UPDATE PHONE:', phone
                        biz.phone = phone
                    if not street_address == '':
                        print 'UPDATE STREET:', street_address
                        biz.address = street_address
                    if not city == '':
                        print 'UPDATE CITY:', city
                        biz.admin3_name = city
                    if not email_primary == '':
                        print 'UPDATE EMAIL:', email_primary
                        biz.contact1_email = email_primary

                    if not extra == '':
                        print '%%%%%%%%%%% EXTRA NOTES %%%%%%%%%%%%%%%'
                        print extra
                        print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'

                    biz.save()

                else:
                    print '@@@@@@@@@@@@@@@@@@ NO BIZ @@@@@@@@@@@@@@@@@@'

            update = False