from directory.models import Business
from django.core.mail import EmailMessage
import urllib
from datetime import datetime, timedelta



def url_with_querystring(path, **kwargs):
    # return path + '?' + urllib.quote(kwargs)
    # return path + '?' + kwargs
    url_params = '&'.join(['%s=%s' % (key, urllib.quote(value)) for (key, value) in kwargs.items()])
    return path + '?' + url_params




def listings_check_in(chunk_start=0, chunk_end=20, days_ago_published=60):
  older_than = datetime.now() - timedelta(days=days_ago_published)

  # find all businesses that are published 90 days or more ago and have email contacts
  #
  # biz = Business.objects.all().filter(contact1_email='damian@airbitz.co')
  biz = Business.objects.all().filter(status='PUB', published__lt=older_than, contact1_email__isnull=False).exclude(contact1_email__exact='')

  # setup typeform vars
  typeform_base_url = 'https://airbitz.typeform.com/to/Sof1Ld'

  # for each of the businesses found build email and send
  for b in biz[chunk_start:chunk_end]:
    listing_screencap = 'https://airbitz.co/media/screencaps/biz-' + str(b.id) + '.jpg'
    listing_url = 'https://airbitz.co/biz/' + str(b.id) + '?v=checkin'
    listing_name = b.name
    listing_website = b.website
    listing_phone = b.phone
    listing_address = b.address
    listing_admin3_name = b.admin3_name
    listing_admin2_name = b.admin2_name
    listing_admin1_code = b.admin1_code
    listing_postalcode = b.postalcode
    listing_contact1_email = b.contact1_email
    listing_contact2_email = b.contact2_email

    typeform_full_url = url_with_querystring( 
      typeform_base_url,
      listingurl=listing_url,
      name=listing_name,
      website=listing_website,
      phone=listing_phone,
      address=listing_address,
      admin3name=listing_admin3_name,
      admin2name=listing_admin2_name,
      admin1code=listing_admin1_code,
      postalcode=listing_postalcode,
      contact1email=listing_contact1_email,
      contact2email=listing_contact2_email,
    )

    typeform_bitcoin_yes = typeform_full_url + '&bitcoin=yes'
    typeform_bitcoin_no = typeform_full_url + '&bitcoin=no'

    email_to = [listing_contact1_email]
    email_from = 'qa@airbitz.co'
    email_subject = 'Still Accepting Bitcoin?'

    msg = EmailMessage(
      to=email_to, 
      from_email=email_from,
      subject=email_subject, 
    )
    msg.template_name = 'business-listing-check-in'
    msg.global_merge_vars = {
      'IMAGE_HEADER_LOGO': 'https://airbitz.co/static/img/logo-email.png',
      'LISTING_URL': listing_url,
      'LISTING_SCREENCAP': listing_screencap,
      'LISTING_NAME': listing_name,
      'BITCOIN_YES': typeform_bitcoin_yes,
      'BITCOIN_NO': typeform_bitcoin_no,
    }

    print 'SENDING TO:', msg.to, 'REGARDING:', listing_name
    msg.send()
    b.last_check_in = datetime.now()
    b.save()
