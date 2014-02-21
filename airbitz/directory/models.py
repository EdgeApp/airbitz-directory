from django.contrib import admin
from django.contrib.gis.db import models
from django.core.files.base import File
from django.utils.formats import time_format
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
import os
import urllib

from airbitz import settings

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
    ("osm", "Open Street Map"),
    ("yelp", "Yelp"),
)

def lookupChoice(value, choices):
    for (i,s) in choices:
        if i == value:
            return s
    return None

def lookupSocialIcon(social_type):
    if social_type == 'facebook':
        social_icon = 'fa-facebook'
    elif social_type == 'foursquare':
        social_icon = 'fa-foursquare'
    elif social_type == 'yelp':
        social_icon = 'fa-comments'
    else:
        social_icon = 'link'
    return social_icon


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

    has_physical_business = models.BooleanField(default=False) # Brick and Mortar?
    has_online_business = models.BooleanField(default=False)
    has_bitcoin_discount = models.DecimalField(default=0.0, decimal_places=3, max_digits=5)

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
        

    def save(self, *args, **kwargs):
        super(Business, self).save()

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

class Sliver(ResizeToFit):
    def __init__(self, width=None, height=None, sliverSize=None):
        super(Sliver, self).__init__(width=width, height=height)
        self.sliverSize = sliverSize

    def process(self, img):
        img = super(Sliver, self).process(img)
        processor = ResizeToFill(width=self.width, height=self.sliverSize)
        return processor.process(img)


class BusinessImage(models.Model):
    image = models.ImageField(upload_to='business_images', 
                              max_length=5000, 
                              height_field='height', 
                              width_field='width')
    mobile_photo = ImageSpecField(source='image',
                              processors=[ResizeToFit(320, 600)],
                              format='JPEG',
                              options={'quality': 60})
    mobile_thumbnail = ImageSpecField(source='image',
                              processors=[Sliver(320, 600, 100)],
                              format='JPEG',
                              options={'quality': 60})
    business = models.ForeignKey(Business, null=False)

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

    def format(self):
        s = ''
        if s != '':
            s += ', ' 
        s += time_format(self.hourStart)
        if self.hourEnd != None:
            s += ' - %s' % time_format(self.hourEnd)
        return s

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

