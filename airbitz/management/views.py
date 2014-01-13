from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from directory.models import Business, BusinessImage, BusinessHours, SocialId
from management.forms import BusinessForm, BizAddressForm, \
                             BizImageForm, BizImageLinkForm, \
                             BizImportForm, HoursFormSet, HoursFormSetHelper, \
                             SocialFormSet, SocialFormHelper

LOGIN_URL='/mgmt/login'

def isManager(u): 
    return u.is_superuser

def login_user(request):
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active and isManager(user):
                login(request, user)
                return HttpResponseRedirect(reverse('mgmt_dashboard'))
        else:
            messages.error(request, 'Authentication failed!')

    return render_to_response('login.html',{
            'username': username
        }, context_instance=RequestContext(request))

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('directory.views.landing')

@user_passes_test(isManager, login_url=LOGIN_URL)
def dashboard(request):
    results = Business.objects.all()
    context = {
        'results': results
    }
    return render_to_response('mgmt_dashboard.html', RequestContext(request, context))

@user_passes_test(isManager, login_url=LOGIN_URL)
def business_import(request):
    if request.method == 'POST':
        form = BizImportForm(request.POST)
        if form.is_valid():
            biz = Business.objects.create()
            social = SocialId.objects.create(business=biz,
                                             social_type='foursquare',
                                             social_id=form.id,
                                             social_url=form.url)
            import foursquare_import as fs
            fs.update_business(biz, social.social_id)
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
def business_view(request, bizId):
    biz = get_object_or_404(Business, pk=bizId)
    hours = BusinessHours.objects.filter(business=biz)
    social = SocialId.objects.filter(business=biz)
    context = {
        'biz': biz,
        'hours': hours,
        'social': social,
        'tab_main': ' class=active ',
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
        form = formclass(request.POST, instance=img)
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes Saved')
            return HttpResponseRedirect(reverse('mgmt_biz_view', args=(biz.id, )))
        else:
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
                img = BusinessImage.create_from_url(biz.id, request.POST['url'])
                messages.success(request, 'Image Saved')
                return HttpResponseRedirect(reverse('mgmt_biz_image_edit', args=(biz.id, img.id)))
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


@user_passes_test(isManager, login_url='account_login')
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

