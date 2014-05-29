import datetime
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.core.files.base import ContentFile
from django.core.files.base import File
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.formats import time_format
from django.utils.http import urlquote_plus
from imagekit.models import ImageSpecField
from rest_framework.authtoken.models import Token
import os
import subprocess
import urllib
import logging

from airbitz import settings
from imgprocessors import DEF_ADMIN_PROC, DEF_MOBILE_PROC

logger = logging.getLogger(__name__)

@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

STATUS_CHOICES = (
    ('DR', 'Draft'),
    ('PUB', 'Published'),
    ('PEN', 'Pending'),
    ('TR', 'Trashed'),
)

DAY_OF_WEEK_CHOICES = (
    ('sunday', 'Sunday'),
    ('monday', 'Monday'),
    ('tuesday', 'Tuesday'),
    ('wednesday', 'Wednesday'),
    ('thursday', 'Thursday'),
    ('friday', 'Friday'),
    ('saturday', 'Saturday'),
)

SOCIAL_TYPES = (
    ("facebook", "Faceboook"),
    ("foursquare", "Foursquare"),
    ("google_plus", "Google+"),
    ("linkedin", "LinkedIn"),
    ("osm", "Open Street Map"),
    ("twitter", "Twitter"),
    ("yelp", "Yelp"),
)

def lookupChoice(value, choices):
    for (i,s) in choices:
        if i == value:
            return s
    return None

def lookupIndex(value, choices):
    for (i,(k,v)) in enumerate(choices):
        if k == value:
            return i
    return 8

def lookupSocialIcon(social_type):
    if social_type == 'facebook':
        social_icon = 'fa-facebook'
    elif social_type == 'foursquare':
        social_icon = 'fa-foursquare'
    elif social_type == 'yelp':
        social_icon = 'fa-comments'
    elif social_type == 'google_plus':
        social_icon = 'fa-google-plus'
    elif social_type == 'twitter':
        social_icon = 'fa-twitter'
    elif social_type == 'linkedin':
        social_icon = 'fa-linkedin'
    else:
        social_icon = 'link'
    return social_icon

def screencap(biz):
    print ''
    print '******* CASPERJS TIME *******'
    print ''
    casper_script = os.getcwd() + '/biz-screen-capture.js'
    casper_save = '--save=' + settings.MEDIA_ROOT + '/screencaps/'
    casper_url = '--url=' + settings.SCREENCAP_ABSOLUTE_URL
    casper_args = ' '.join(['/home/devbitz/local/bin/casperjs', casper_script, casper_save, casper_url, str(biz.id)])
    logger.debug("this is a debug message!")
    print casper_args
    try:
        print subprocess.check_output(
            casper_args,
            shell=True,
            stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as e:
        print e

class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=2500, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{0}".format(self.name)

class ImageTag(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=2500, null=True)

    def __unicode__(self):
        return "{0}".format(self.name)

class Business(models.Model):
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default='DR')
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(max_length=2000, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    neighborhood = models.CharField(max_length=200, blank=True, null=True)
    admin3_name = models.CharField(max_length=200, blank=True, null=True) # City
    admin2_name = models.CharField(max_length=200, blank=True, null=True) # County
    admin1_code = models.CharField(max_length=200, blank=True, null=True) # State
    postalcode = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True, null=True)
    landing_image = models.ForeignKey('BusinessImage', null=True, blank=True, 
                                      on_delete=models.SET_NULL, related_name='landing_image_business')
    mobile_landing_image = models.ForeignKey('BusinessImage', null=True, blank=True, 
                                      on_delete=models.SET_NULL, related_name='mobile_landing_image')

    has_physical_business = models.BooleanField(default=False) # Brick and Mortar?
    has_online_business = models.BooleanField(default=False)
    has_bitcoin_discount = models.DecimalField(default=0.0, decimal_places=3, max_digits=5)

    contact1_email = models.EmailField(blank=True)
    contact2_email = models.EmailField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(blank=True, null=True)

    last_modified_by = models.CharField(max_length=200, blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)

    # PostGis fields
    center = models.PointField(blank=True, null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return u'%s (id=%s)' % (self.name, self.pk)

    @property
    def lookupStatus(self):
        return lookupChoice(self.status, STATUS_CHOICES)

    @property
    def pretty_address(self):
        s = ''
        if self.address:
            s = self.address
        if self.admin3_name:
            if len(s) > 0: s+= ', '
            s += self.admin3_name 
        if self.admin2_name:
            if len(s) > 0: s+= ', '
            s += self.admin2_name 
        if self.admin1_code:
            if len(s) > 0: s+= ', '
            s += self.admin1_code 
        return s

    @property
    def gmap_directions_url(self):
        gmaps_url = 'https://maps.google.com/maps?saddr=my+location&daddr='
        if self.center:
            lat, lon = self.center.y, self.center.x
        else:
            lat, lon = None, None

        if self.address:
            destination = self.address + ' ' + self.admin3_name + ' ' + self.admin1_code
        elif lat and lon:
            destination = 'loc:' + str(lat) + ' ' + str(lon)
        else:
            destination = self.name
        return gmaps_url + urlquote_plus(destination)

    # override default save and check for published to set a publish date
    def save(self, *args, **kwargs):
        try:
            orig = Business.objects.get(pk=self.pk)
            if orig.status == 'PUB':
                if self.published == None:
                    self.published = datetime.datetime.now()
            else:
                if self.status == 'PUB':
                    self.published = datetime.datetime.now()
                else:
                    self.published = None
        except Business.DoesNotExist:
            pass
		
		if self.status == 'PUB':
			screencap(self)

        super(Business, self).save(*args, **kwargs)

class SocialId(models.Model):
    business = models.ForeignKey(Business, null=False)
    social_type = models.CharField(max_length=50, null=True, blank=True)
    social_id = models.CharField(max_length=200, null=True, blank=True)
    social_url = models.URLField(max_length=2000, null=True, blank=True)

    @property
    def lookupType(self):
        return lookupChoice(self.social_type, SOCIAL_TYPES)

    @property
    def social_icon(self):
        return lookupSocialIcon(self.social_type);

class BusinessImage(models.Model):
    image = models.ImageField(upload_to='business_images', 
                              max_length=5000, 
                              height_field='height', 
                              width_field='width')
    admin_photo = ImageSpecField(source='image',
                              processors=[DEF_ADMIN_PROC],
                              format='JPEG',
                              options={'quality': 60})
    business = models.ForeignKey(Business, null=False)

    mobile_photo_x1 = models.PositiveIntegerField(blank=True, null=True)
    mobile_photo_y1 = models.PositiveIntegerField(blank=True, null=True)
    mobile_photo_x2 = models.PositiveIntegerField(blank=True, null=True)
    mobile_photo_y2 = models.PositiveIntegerField(blank=True, null=True)

    web_photo_x1 = models.PositiveIntegerField(blank=True, null=True)
    web_photo_y1 = models.PositiveIntegerField(blank=True, null=True)
    web_photo_x2 = models.PositiveIntegerField(blank=True, null=True)
    web_photo_y2 = models.PositiveIntegerField(blank=True, null=True)

    web_photo = ImageSpecField(source='image', id='ab:image:web_crop')
    mobile_photo = ImageSpecField(source='image', processors=[DEF_MOBILE_PROC])
    mobile_thumbnail = ImageSpecField(source='image', id='ab:image:mobile_crop')

    height = models.PositiveIntegerField(null=True)
    width = models.PositiveIntegerField(null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(ImageTag, blank=True, null=True)

    @staticmethod
    def create_from_url(bizId, img_url):
        result = urllib.urlretrieve(img_url)
        img = BusinessImage()
        img.image_url = img_url
        img.business_id = bizId
        img.image.save(os.path.basename(img_url), File(open(result[0])))
        img.save()
        return img

    def duplicate(self, biz):
        tags = self.tags.all()

        img = BusinessImage()
        f = ContentFile(self.image.read())
        f.name = self.image.name
        img.image = f
        img.height = self.height
        img.width = self.width
        img.mobile_photo_x1 = self.mobile_photo_x1
        img.mobile_photo_y1 = self.mobile_photo_y1
        img.mobile_photo_x2 = self.mobile_photo_x2
        img.mobile_photo_y2 = self.mobile_photo_y2
        img.web_photo_x1 = self.web_photo_x1
        img.web_photo_y1 = self.web_photo_y1
        img.web_photo_x2 = self.web_photo_x2
        img.web_photo_y2 = self.web_photo_y2

        img.business = biz
        img.save()

        for t in tags:
            img.tags.add(t)
        img.save()
        return img

    def get_absolute_url(self):
        return os.path.join(settings.MEDIA_URL, self.image.url)

    @property
    def name(self):
        return os.path.basename(self.image.name)

    @property
    def url(self):
        return os.path.join(settings.MEDIA_URL, self.image.url)

    def save(self, *args, **kwargs):
        super(BusinessImage, self).save(*args, **kwargs)

class BusinessHours(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    business = models.ForeignKey(Business, null=False)
    dayOfWeek = models.CharField(max_length=30, choices=DAY_OF_WEEK_CHOICES)
    hourStart = models.TimeField(blank=True, null=True)
    hourEnd = models.TimeField(blank=True, null=True)

    @property
    def lookupDayOfWeek(self):
        return lookupChoice(self.dayOfWeek, DAY_OF_WEEK_CHOICES)

    @property
    def lookupDayNumber(self):
        return lookupIndex(self.dayOfWeek, DAY_OF_WEEK_CHOICES)

    def format(self):
        s = ''
        if s != '':
            s += ', ' 
        s += time_format(self.hourStart)
        if self.hourEnd != None:
            s += ' - %s' % time_format(self.hourEnd)
        return s

    def __unicode__(self):
        return u'%s (day=%s)' % (self.business, self.dayOfWeek)


class BusinessAdmin(admin.ModelAdmin):
    pass

class BusinessImageAdmin(admin.ModelAdmin):
    pass

class BusinessHoursAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Business, BusinessAdmin)
admin.site.register(BusinessImage, BusinessImageAdmin)
admin.site.register(BusinessHours, BusinessHoursAdmin)

