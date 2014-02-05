from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Field, Submit
from django.core import validators
from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.gis import forms as geoforms
from django.utils.translation import ugettext as _

from directory.models import Business, BusinessImage, BusinessHours, \
                             ImageTag, Category, SocialId, SOCIAL_TYPES

class LatLongWidget(forms.MultiWidget):
    def __init__(self, attrs=None, date_format=None, time_format=None):
        widgets = (forms.TextInput(attrs=attrs),
                   forms.TextInput(attrs=attrs))
        super(LatLongWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return tuple(reversed(value.coords))
        return (None, None)

class LatLongField(forms.MultiValueField):
    widget = LatLongWidget
    srid = 4326

    default_error_messages = {
        'invalid_latitude' : _('Enter a valid latitude.'),
        'invalid_longitude' : _('Enter a valid longitude.'),
    }
    def __init__(self, *args, **kwargs):
        fields = (forms.FloatField(min_value=-90, max_value=90), 
                  forms.FloatField(min_value=-180, max_value=180))
        super(LatLongField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            if data_list[0] in validators.EMPTY_VALUES:
                raise forms.ValidationError(self.error_messages['invalid_latitude'])
            if data_list[1] in validators.EMPTY_VALUES:
                raise forms.ValidationError(self.error_messages['invalid_longitude'])
            srid_str = 'SRID=%d'%self.srid
            point_str = 'POINT(%f %f)'%tuple(reversed(data_list))
            return ';'.join([srid_str, point_str])
        return None

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ( "name",
                   "description", 
                 )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Field('name', css_class='input-xxlarge'),
            Field('description', css_class='input-xxlarge'),
            FormActions(
                Submit('submit', 'Save', css_class='btn btn-success'),
            )
        )
        super(CategoryForm, self).__init__(*args, **kwargs)

class ImageTagForm(forms.ModelForm):
    class Meta:
        model = ImageTag
        fields = ( "name",
                   "description", 
                 )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Field('name', css_class='input-xxlarge'),
            Field('description', css_class='input-xxlarge'),
            FormActions(
                Submit('submit', 'Save', css_class='btn btn-success'),
            )
        )
        super(ImageTagForm, self).__init__(*args, **kwargs)

class BizImportForm(forms.Form):
    id = forms.CharField(label='FS Id: ', required=True)
    url = forms.URLField(label='FS URL: ', required=True)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Field('id'),
            Field('url'),
            FormActions(
                Submit('submit', 'Import', css_class='btn btn-success'),
            )
        )
        super(BizImportForm, self).__init__(*args, **kwargs)

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ( "status",
                   "name", 
                   "categories",
                   "description",
                   "phone",
                   "website",
                   "has_physical_business",
                   "has_online_business",
                   "has_bitcoin_discount",
                 )

    def __init__(self, *args, **kwargs):
        catSet = Category.objects.all().order_by('title')
        self.categories = forms.ModelMultipleChoiceField(queryset=catSet)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Field('status'),
            Field('name', css_class='input-xxlarge'),
            Field('categories'),
            Field('phone'),
            Field('website'),
            Field('has_physical_business'),
            Field('has_online_business'),
            Field('has_bitcoin_discount'),
            Field('description', css_class='input-xxlarge'),
            FormActions(
                Submit('submit', 'Save', css_class='btn btn-success'),
            )
        )
        super(BusinessForm, self).__init__(*args, **kwargs)


class BizAddressForm(geoforms.ModelForm):
    center = LatLongField(label="Latitude/Longitude", required=False)
    admin3_name = forms.CharField(label='City: ', required=False)
    admin2_name = forms.CharField(label='County: ', required=False)
    admin1_code = forms.CharField(label='State: ', required=False)
    class Meta:
        model = Business
        fields = ( "address",
                   "admin3_name", 
                   "admin2_name", 
                   "admin1_code",
                   "postalcode",
                   "country",
                   "center"
                 )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Field('address', css_class='input-xxlarge'),
            Field('admin3_name', css_class='input-xxlarge'),
            Field('admin2_name', css_class='input-xxlarge'),
            Field('admin1_code'),
            Field('postalcode'),
            Field('country'),
            Field('center'),
            FormActions(
                Submit('submit', 'Save', css_class='btn btn-success'),
            )
        )
        super(BizAddressForm, self).__init__(*args, **kwargs)

class BizImageForm(forms.ModelForm):
    class Meta:
        model = BusinessImage
        fields = ("image", "tags", )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            HTML("""{% if form.image.value %}<img class="img-responsive" src="{{ MEDIA_URL }}{{ form.image.value }}">{% endif %}""", ),
            Field('image'),
            Field('tags'),
            FormActions(
                Submit('submit', 'Save', css_class='btn btn-success'),
            )
        )
        super(BizImageForm, self).__init__(*args, **kwargs)

class BizImageLinkForm(forms.Form):
    url = forms.URLField(label='Image URL: ', required=True)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Field('url'),
            FormActions(
                Submit('submit', 'Save', css_class='btn btn-success'),
            )
        )
        super(BizImageLinkForm, self).__init__(*args, **kwargs)


class SocialForm(forms.ModelForm):
    social_type = forms.ChoiceField(choices=SOCIAL_TYPES)
    class Meta:
        model = SocialId
        fields=("social_type", "social_id", "social_url", )

class SocialFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(SocialFormHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            'social_type',
            'social_id',
            'social_url',
        )
        self.render_required_fields = True,
        self.template = 'bootstrap/table_inline_formset.html'
        self.add_input(Submit("submit", "Save"))

SocialFormSet = inlineformset_factory(Business, SocialId, form=SocialForm, extra=1, can_delete=False)

class HoursForm(forms.ModelForm):
    class Meta:
        model = BusinessHours
        fields=("dayOfWeek", "hourStart", "hourEnd", )

class HoursFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(HoursFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            'dayOfWeek',
            'hourStart',
            'hourEnd',
        )
        self.render_required_fields = True,
        self.template = 'bootstrap3/table_inline_formset.html'
        self.add_input(Submit("submit", "Save"))

HoursFormSet = inlineformset_factory(Business, BusinessHours, form=HoursForm, extra=1, can_delete=False)


