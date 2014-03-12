from imagekit.processors import ResizeToFill, ResizeToFit, Crop, Thumbnail
from imagekit import ImageSpec, register
from imagekit.utils import get_field_info
from pilkit.processors import Adjust, MakeOpaque

class Sliver(ResizeToFit):
    def __init__(self, width=None, height=None, sliverSize=None):
        super(Sliver, self).__init__(width=width, height=height)
        self.sliverSize = sliverSize

    def process(self, img):
        img = super(Sliver, self).process(img)
        processor = ResizeToFill(width=self.width, height=self.sliverSize)
        return processor.process(img)

class ResizeToDimensions(Crop):
    def __init__(self, obj):
        self.obj = obj

    def process(self, img):
        obj = self.obj
        crop = Crop(x=obj.mobile_photo_x1, y=obj.mobile_photo_y1, 
                    width=obj.mobile_photo_x2 - obj.mobile_photo_x1,
                    height=obj.mobile_photo_y2 - obj.mobile_photo_y1)
        return crop.process(img)

class GalleryThumbnail(ImageSpec):
    processors = [ResizeToFit(260,400)]
    format = 'JPEG'
    options = {'quality': 80}

register.generator('ab:gallerythumb', GalleryThumbnail)

DEF_WEB_W, DEF_WEB_H = 300, 300
DEF_MOB_W, DEF_MOB_H = 640, 320
DEF_ADMIN_PROC=ResizeToFit(800, 800, upscale=False, mat_color="#FFF")
DEF_MOBILE_PROC=ResizeToFit(640, 1136, mat_color=(255, 255, 255, 255))

class ResizeWebToDimensions(object):
    def __init__(self, obj, imgid, x1, y1, x2, y2):
        self.obj = obj
        self.imgid = imgid
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def process(self, img):
        obj = self.obj
        x, y = obj.web_photo_x1, obj.web_photo_y1
        width = obj.web_photo_x2 - obj.web_photo_x1
        height = obj.web_photo_y2 - obj.web_photo_y1
        img = img.crop((x, y, x + width, y + height))
        p = ResizeToFill(DEF_WEB_W, DEF_WEB_H)
        return p.process(img)

class WebCrop(ImageSpec):
    format = 'JPEG'
    options = {'quality': 60}

    @property
    def processors(self):
        model, _ = get_field_info(self.source)
        if model.web_photo_x1 and model.web_photo_y1:
            r = ResizeWebToDimensions(model, model.id, 
                    model.web_photo_x1, model.web_photo_y1,
                    model.web_photo_x2, model.web_photo_y2)
            return [DEF_ADMIN_PROC, r]
        else:
            return [Thumbnail(width=DEF_WEB_W, height=DEF_WEB_H, upscale=True)]

class ResizeMobileToDimensions(object):
    def __init__(self, obj, imgid, x1, y1, x2, y2):
        self.obj = obj
        self.imgid = imgid
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def process(self, img):
        obj = self.obj
        x, y = obj.mobile_photo_x1, obj.mobile_photo_y1
        width = obj.mobile_photo_x2 - obj.mobile_photo_x1
        height = obj.mobile_photo_y2 - obj.mobile_photo_y1
        img = img.crop((x, y, x + width, y + height))
        p = ResizeToFill(DEF_MOB_W, DEF_MOB_H)
        return p.process(img)

class MobileCrop(ImageSpec):
    format = 'JPEG'
    options = {'quality': 60}

    @property
    def processors(self):
        model, _ = get_field_info(self.source)
        if model.mobile_photo_x1 and model.mobile_photo_y1:
            r = ResizeMobileToDimensions(model, model.id, 
                    model.mobile_photo_x1, model.mobile_photo_y1,
                    model.mobile_photo_x2, model.mobile_photo_y2)
            return [DEF_ADMIN_PROC, r]
        else:
            return [Thumbnail(width=DEF_MOB_W, height=DEF_MOB_H, upscale=True)]

register.generator('ab:image:web_crop', WebCrop)
register.generator('ab:image:mobile_crop', MobileCrop)

# TODO: Tried to get a guassian blur to work server side (ideal solution) but
# couldn't figure out how to add other processors
class TopBgBlurred(ImageSpec):
    processors = ProcessorPipeline = ([
        Adjust(sharpness=0.5),
        MakeOpaque()
    ])
    format = 'JPEG'
    options = {'quality': 80}

register.generator('ab:topbgblurred', TopBgBlurred)

