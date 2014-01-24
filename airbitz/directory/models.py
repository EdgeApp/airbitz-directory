from django.contrib import admin
from django.core.files.base import File
from django.contrib.gis.db import models
from django.utils.formats import time_format
import os
import urllib

from airbitz import settings

STATUS_CHOICES = (
    ('DR', 'Draft'),
    ('PUB', 'Published'),
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

def lookupChoice(value, choices):
    for (i,s) in choices:
        if i == value:
            return s
    return None

class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=2500, null=True)

    def __unicode__(self):
        return "{0}".format(self.name)

class Business(models.Model):
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default='DR')
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=False, null=True)
    website = models.URLField(max_length=2000, blank=False, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    postalcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, null=True)
    landing_image = models.ForeignKey('BusinessImage', null=True, blank=True, 
                                      on_delete=models.SET_NULL, related_name='landing_image_business')

    has_physical_business = models.BooleanField(default=False) # Brick and Mortar?
    has_online_business = models.BooleanField(default=False)
    has_bitcoin_discount = models.BooleanField(default=False)

    # PostGis fields
    center = models.PointField(null=True)
    objects = models.GeoManager()

    @property
    def lookupStatus(self):
        return lookupChoice(self.status, STATUS_CHOICES)

    @property
    def pretty_address(self):
        s = ''
        if self.address:
            s = self.address
        if self.city:
            s += ', ' + self.city 
        return s
        

    def save(self, *args, **kwargs):
        super(Business, self).save()

class SocialId(models.Model):
    business = models.ForeignKey(Business, null=False)
    social_type = models.CharField(max_length=50, null=True)
    social_id = models.CharField(max_length=200, null=True)
    social_url = models.URLField(max_length=2000, null=True)

class BusinessImage(models.Model):
    image = models.ImageField(upload_to='business_images', 
                              max_length=5000, 
                              height_field='height', 
                              width_field='width')
    business = models.ForeignKey(Business, null=False)
    height = models.PositiveIntegerField(null=True)
    width = models.PositiveIntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

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
    hourStart = models.TimeField()
    hourEnd = models.TimeField()

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

