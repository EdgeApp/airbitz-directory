from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from directory.models import STATUS_CHOICES, SOCIAL_TYPES, \
                             Category, ImageTag, \
                             Business, BusinessImage, \
                             BusinessHours, SocialId
from management.forms import CategoryForm, ImageTagForm, \
                             BusinessForm, BizAddressForm, \
                             BizImageForm, BizImageLinkForm, \
                             BizImportForm, HoursFormSet, HoursFormSetHelper, \
                             SocialFormSet, SocialFormHelper
from time import strftime

LOGIN_URL='/mgmt/login'

def isManager(u): 
    return u.is_superuser

def login_user(request):
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            if isManager(user):
                login(request, user)
                return HttpResponseRedirect(reverse('mgmt_dashboard'))
            else:
                login(request, user)
                return HttpResponseRedirect(reverse('landing'))
        else:
            messages.error(request, 'Authentication failed!')

    return render_to_response('login.html',{
            'username': username
        }, context_instance=RequestContext(request))

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('landing'))

@user_passes_test(isManager, login_url=LOGIN_URL)
def dashboard(request):
    context = {
        'STATUS_CHOICES': STATUS_CHOICES
    }
    return render_to_response('mgmt_dashboard.html', RequestContext(request, context))

@user_passes_test(isManager, login_url=LOGIN_URL)
def map(request):
    context = {
        'STATUS_CHOICES': STATUS_CHOICES
    }
    return render_to_response('mgmt_map_view.html', RequestContext(request, context))

@user_passes_test(isManager, login_url=LOGIN_URL)
def category_list(request):
    results = Category.objects.all()
    context = {
        'cats': results
    }
    return render_to_response('mgmt_category_list.html', RequestContext(request, context))

@user_passes_test(isManager, login_url=LOGIN_URL)
def image_tag_list(request):
    results = ImageTag.objects.all()
    context = {
        'tags': results
    }
    return render_to_response('mgmt_image_tag_list.html', RequestContext(request, context))

@user_passes_test(isManager, login_url=LOGIN_URL)
def category_edit(request, catId=None):
    return object_edit(request, title='Category Edit',
                       objId=catId, objclass=Category, \
                       objform=CategoryForm, returnUrl='mgmt_category_list')

@user_passes_test(isManager, login_url=LOGIN_URL)
def category_delete(request, catId=None):
    obj = get_object_or_404(Category, pk=catId)
    obj.delete()
    messages.success(request, 'Category deleted')
    return HttpResponseRedirect(reverse('mgmt_category_list'))

@user_passes_test(isManager, login_url=LOGIN_URL)
def image_tag_edit(request, tagId=None):
    return object_edit(request, title='Image Tag Edit',
                       objId=tagId, objclass=ImageTag,
                       objform=ImageTagForm, returnUrl='mgmt_image_tag_list')

@user_passes_test(isManager, login_url=LOGIN_URL)
def image_tag_delete(request, tagId=None):
    obj = get_object_or_404(ImageTag, pk=tagId)
    obj.delete()
    messages.success(request, 'Tag deleted')
    return HttpResponseRedirect(reverse('mgmt_image_tag_list'))

@user_passes_test(isManager, login_url=LOGIN_URL)
def object_edit(request, title=None, objId=None, objclass=None, \
                objform=None, returnUrl=None):
    if objId:
        obj = get_object_or_404(objclass, pk=objId)
    else:
        obj = objclass()
    if request.method == 'POST':
        form = objform(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes Saved')
            return HttpResponseRedirect(reverse(returnUrl))
        else:
            messages.error(request, 'Unable to save record.')
    else:
        form = objform(instance=obj)

    return render(request, 'mgmt_biz_edit.html', {
        'title': title,
        'obj': obj,
        'form': form,
    })

@user_passes_test(isManager, login_url=LOGIN_URL)
def business_import(request):
    if request.method == 'POST':
        form = BizImportForm(request.POST)
        if form.is_valid():
            fsid = form.cleaned_data['id']
            fsurl = form.cleaned_data['url']
            biz = Business.objects.create()
            social = SocialId.objects.create(business=biz,
                                             social_type='foursquare',
                                             social_id=fsid,
                                             social_url=fsurl)
            import foursquare_import as fs
            importer = fs.FoursquareClient()
            importer.update_business(biz, social.social_id)
            messages.success(request, 'Place Imported')
            return HttpResponseRedirect(reverse('mgmt_biz_view', args=(biz.id, )))
        else:
            messages.error(request, 'Unable to save record.')
    else:
        form = BizImportForm()
    return render(request, 'mgmt_biz_edit.html', {
        'form': form,
    })


@user_passes_test(isManager, login_url=LOGIN_URL)
def business_base_edit(request, bizId=None):
    return business_edit(request, bizId=bizId, formclass=BusinessForm) 

@user_passes_test(isManager, login_url=LOGIN_URL)
def business_location_edit(request, bizId=None):
    return business_edit(request, bizId=bizId, formclass=BizAddressForm) 

def business_edit(request, bizId=None, formclass=None):
    if bizId:
        biz = get_object_or_404(Business, pk=bizId)
    else:
        biz = Business()
    if request.method == 'POST':
        form = formclass(request.POST, instance=biz)
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes Saved')
            return HttpResponseRedirect(reverse('mgmt_biz_view', args=(biz.id, )))
        else:
            messages.error(request, 'Unable to save record.')
    else:
        form = formclass(instance=biz)

    return render(request, 'mgmt_biz_edit.html', {
        'title': 'Add/Edit',
        'biz': biz,
        'form': form,
    })

@user_passes_test(isManager, login_url=LOGIN_URL)
def business_copy(request, bizId):
    biz = get_object_or_404(Business, pk=bizId)
    categories = biz.categories.all()
    socials = biz.socialid_set.all()
    hours = biz.businesshours_set.all()
    images = biz.businessimage_set.all()

    biz.pk = None
    biz.save()
    for c in categories:
        biz.categories.add(c)
    for s in socials:
        s.pk = None
        s.business = biz
        s.save()
    for h in hours:
        h.pk = None
        h.business = biz
        h.save()
    for i in images:
        i.duplicate(biz)
    return HttpResponseRedirect(reverse('mgmt_biz_view', args=(biz.id, )))

@user_passes_test(isManager, login_url=LOGIN_URL)
def business_view(request, bizId):
    biz = get_object_or_404(Business, pk=bizId)
    hours = BusinessHours.objects.filter(business=biz)
    social = SocialId.objects.filter(business=biz)

    if biz.published is None:
        published = ''
    else:
        published = biz.published.strftime('%m/%d/%y %H:%M:%S')

    context = {
        'STATUS_CHOICES': STATUS_CHOICES,
        'SOCIAL_TYPES': SOCIAL_TYPES,
        'biz': biz,
        'hours': hours,
        'social': social,
        'tab_main': ' class=active ',
        'created': biz.created.strftime('%m/%d/%y %H:%M:%S'),
        'modified': biz.modified.strftime('%m/%d/%y %H:%M:%S'),
        'published': published,
    }
    return render_to_response('mgmt_biz_view.html', RequestContext(request, context))

@user_passes_test(isManager, login_url=LOGIN_URL)
def business_image_view(request, bizId):
    biz = get_object_or_404(Business, pk=bizId)
    images = BusinessImage.objects.filter(business=biz)
    context = {
        'biz': biz,
        'images': images,
        'tab_images': ' class=active ',
    }
    return render_to_response('mgmt_biz_image_view.html', RequestContext(request, context))

def business_image_edit(request, bizId, imgId=None):
    formclass = BizImageForm
    biz = get_object_or_404(Business, pk=bizId)
    if imgId:
        img = get_object_or_404(BusinessImage, pk=imgId)
    else:
        img = BusinessImage()
    img.business = biz
    if request.method == 'POST':
        form = formclass(request.POST, request.FILES, instance=img)
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes Saved')
            return HttpResponseRedirect(reverse('mgmt_biz_view', args=(biz.id, )))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print field, error
            messages.error(request, 'Unable to save record.')
    else:
        form = formclass(instance=img)

    return render(request, 'mgmt_biz_edit.html', {
        'title': 'Add/Edit',
        'biz': biz,
        'img': img,
        'form': form,
    })
    
@user_passes_test(isManager, login_url=LOGIN_URL)
def business_image_link(request, bizId):
    biz = get_object_or_404(Business, pk=bizId)
    if request.method == 'POST':
        form = BizImageLinkForm(request.POST)
        if form.is_valid():
            try:
                BusinessImage.create_from_url(biz.id, request.POST['url'])
                messages.success(request, 'Image Saved')
                return HttpResponseRedirect(reverse('mgmt_biz_view', args=(biz.id, )))
            except:
                messages.error(request, 'Unable to save record.')
        else:
            messages.error(request, 'Unable to save record.')
    else:
        form = BizImageLinkForm()

    return render(request, 'mgmt_biz_edit.html', {
        'biz': biz,
        'form': form,
        'title': 'Image Link',
    })


@user_passes_test(isManager, login_url=LOGIN_URL)
def set_landing_image(request, bizId, imgId):
    biz = get_object_or_404(Business, pk=bizId)
    img = get_object_or_404(BusinessImage, pk=imgId)
    if request.method == 'POST':
        biz.landing_image = img
        biz.save()
        return HttpResponse('Nice pic')
    else: 
        return HttpResponse('POSTS only boys')

@user_passes_test(isManager, login_url=LOGIN_URL)
def business_hours_edit(request, bizId):
    return generic_biz_edit(request, bizId, 
                      formClass=HoursFormSet,
                      stayView='mgmt_biz_hours_edit',
                      helper=HoursFormSetHelper,
                      title='Edit Hours')

@user_passes_test(isManager, login_url=LOGIN_URL)
def business_social_edit(request, bizId):
    return generic_biz_edit(request, bizId, 
                      formClass=SocialFormSet,
                      stayView='mgmt_biz_social_edit',
                      helper=SocialFormHelper,
                      title='Edit Social')


@user_passes_test(isManager, login_url=LOGIN_URL)
def generic_biz_edit(request, bizId, title, formClass,
                     template='mgmt_biz_edit.html',
                     stayView='mgmt_biz_view',
                     helper=None,
                     returnUrl=None,
                     extras={}):
    biz = get_object_or_404(Business, pk=bizId)
    if helper:
        h = helper()
    else:
        h = None
    if request.method == 'POST':
        form = formClass(request.POST, instance=biz)
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes Saved')
            if returnUrl:
                return HttpResponseRedirect(returnUrl)
            else:
                return HttpResponseRedirect(reverse(stayView, args=(biz.id, )))
        else:
            messages.error(request, 'Unable to save record.')
    else:
        form = formClass(instance=biz)

    context = {
        'title': title,
        'biz': biz,
        'helper': h,
        'form': form,
    }
    return render(request, template, dict(context.items() + extras.items()))

@user_passes_test(isManager, login_url=LOGIN_URL)
def image_delete(request, bizId, imgId):
    if request.method == 'DELETE':
        get_object_or_404(Business, pk=bizId)
        get_object_or_404(BusinessImage, pk=imgId).delete()
        messages.success(request, 'Image deleted')
        return HttpResponseRedirect(reverse('mgmt_biz_image_view', args=(bizId, )))
    else:
        raise Http404


# QUICK REDIRECTIONS (PROBABLY SHOULD BE ITS OWN APP EVENTUALLY)
def redirect_vote(request):
    return HttpResponseRedirect('https://docs.google.com/a/airbitz.co/forms/d/1XGPghf1OsdgTmrsiEscWqcPjssfDX3u8IE-PBOLebc4/viewform')

def redirect_blog(request):
    return HttpResponseRedirect('https://go.airbitz.co')

def redirect_about(request):
    return HttpResponseRedirect('https://go.airbitz.co/about/')

def redirect_button(request):
    return HttpResponseRedirect('https://airbitz.co/')

