import datetime
from django.contrib.gis.measure import D
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from airbitz import regions_data
from airbitz.regions_data import ACTIVE_REGIONS, ALL_REGIONS
from airbitz.settings import GOOGLE_MAP_KEY
from directory.models import Business, BusinessImage, SocialId
from directory.models import STATUS_CHOICES, SOCIAL_TYPES
from restapi import api
from restapi.serializers import calc_distance

SEARCH_LIMIT = 20
DISTANCE_LIMIT_KILOMETERS = 20
SPECIALS_TAG='Bitcoin Bowl'

WEEKDAYS = (
    ('sunday', 'Sun'),
    ('monday', 'Mon'),
    ('tuesday', 'Tue'),
    ('wednesday', 'Wed'),
    ('thursday', 'Thu'),
    ('friday', 'Fri'),
    ('saturday', 'Sat'),
)


def get_biz_hours(biz):
    days_hours = biz.businesshours_set.all()
    midnight = datetime.time(0,0,0)
    week_of_hours = {}

    for weekday in WEEKDAYS:
        week_of_hours[weekday[1]] = ''

        for dh in days_hours:
            if dh.dayOfWeek == weekday[0]: # matched on the day of week so add the hours to that dict key
                if (dh.hourStart == midnight and dh.hourEnd == None) \
                    or (dh.hourStart == None and dh.hourEnd == None): # if matched this day was open 24hr
                    week_of_hours[weekday[1]] = ['Open 24hr', None]
                else:
                    week_of_hours[weekday[1]] = [dh.hourStart, dh.hourEnd]

    return week_of_hours

def get_biz(request, *args, **kwargs):
    # print 'QUERY ARGS:', args
    # print 'QUERY KWARGS:', kwargs
    biz = get_object_or_404(Business, **kwargs)
    # print biz

    if request.user.is_superuser or biz.status == 'PUB':
        return biz
    else:
        raise Http404

def home_v2(request):
    return render_to_response('home-v2.html', RequestContext(request, {}))

def landing_v2(request):
    print 'OLD LANDING'

    team_info_row_1 = [
        {
            "name": "Paul Puey",
            "img_path": "airbitz-theme/img-custom/portraits/paul.jpg",
            "title": "CEO / Co-Founder",
            "nickname": "Cheif Inspirator",
            "bio_html": "<p>Paul is a proud Electrical Engineering and Computer Science graduate of UC Berkeley with a wide range of technical skills from low-level 3D graphics engineering to development of custom web CMS systems, even before people knew what a CMS was. He held lead engineering positions with Nvidia and Chromatic Research, but most recently owned and operated several non-technical small businesses throughout California. There he learned the importance of the intersection of people, business, and technology.</p><p>Today, Paul aims to bring Bitcoin mainstream with software and products aimed at simplifying Bitcoin and making it insanely easy to send and secure this revolutionary currency while maintaining the highest level of privacy.</p><p>When not converting people to bitcoin you'll likely find him climbing a rock in Joshua Tree or at a local climbing gym.</p>",
            "skills": ["Software Architecture", "Business Development", "UI/UX", "Bitcoin Community Evangelist"]
        },
        {
            "name": "Tim Horton",
            "img_path": "airbitz-theme/img-custom/portraits/tim.jpg",
            "title": "CTO / Co-Founder",
            "nickname": "Code Gigolo",
            "bio_html": "<p>Tim began working as a software developer in 2005 in the finance industry. In 2007, during the turbulent markets, his software and the engineering department was acquired. He continued working in the finance industry while receiving his masters in Computer Science from California State University of San Marcos, focusing on applying machine learning to problems in BioInformatics.</p><p>In 2012, he co-founded Breadcrumbs, a mobile app to track your time and where you spend it. Breadcrumbs received awards at Uplinq 2012 conference, $50k in seed investment, and were accepted to the Qualcomm Labs EvoNexus startup incubator program in San Diego.</p><p>Tim has now turned his interest to all thing crypto. But when he isn't hashing and twiddling bits, he also enjoys traveling, backpacking and playing guitar.</p>",
            "skills": ["System Administration", "Java", "Python", "C"]
        },
        {
            "name": "Rick \"Henri\" Chan",
            "img_path": "airbitz-theme/img-custom/portraits/rick.jpg",
            "title": "Cheif Operating Officer",
            "nickname": "Worldwide Deal Wizard",
            "bio_html": "<p>Rick thrives on putting things together in a unique way and brings a diverse background to Airbitz. After graduating from the University of Rochester with a B.S. in Optics, Rick spent four years working in the Optical Engineering field before moving on to grad school. At Thunderbird, he specialized in Finance and International Management.</p><p>Since grad school, Rick has successfully connected investors, tech and great opportunities as he worked with a variety of startups, global FinTech ventures and Wall Streeters. Rick brings extensive startup experience in mobile, tech, social media, gaming, gamification, entertainment, FinTech and Bitcoin. He was a co-founder of AlphaPoint and served as COO. In addition, Rick's extensive knowledge of boutiques and Fortune 500 companies adds a broad perspective. Name a financial center around the world and Rick has probably been there, but there are still so many more to explore!</p><p>Rick loves scuba diving in tropical water. He is also a bokeholic.</p>",
            "skills": ["Serial Entrepreneur", "Broad Startup Experience", "Global FinTech", "International Wall St & BTC Passion"]
        },
        {
            "name": "William Swanson",
            "img_path": "airbitz-theme/img-custom/portraits/william.jpg",
            "title": "Cheif Architect / Co-Founder",
            "nickname": "Code Plumber",
            "bio_html": '<p>William Swanson has been writing software since he was 11 years old. Although he has a degree in Electical Engineering from Cal Poly San Luis Obispo, he is just as comfortable working with software as he is with electronics. He has built systems at every level of the technology stack, from custom circuit boards with embedded firmware up through web sites and 3D graphics applications.</p><p>Through his work with AirBitz, William Swanson has become an official contributor to the <a href="http://libbitcoin.dyne.org/">libbitcoin</a> project, where he has written and contributed several new functional modules.</p><p>In April 2014 William teamed up with Amir Taaki, Pablo Martin of the Libbitcoin and <a href="http://darkwallet.is">DarkWallet</a> project along with Damian Cutillo of Airbitz in Toronto for the <a href="http://bitcoinexpo.ca/hackathon/">2014 Bitcoin Expo Hackathon</a>. The team won first place with the <a href="https://airbitz.co/go/airbitz-dark-wallet-win-bitcoin-hackathon-darkmarket/">DarkMarket</a> project, a proof of concept for one of the world\'s first fully decentralized, anonymous, peer to peer marketplaces. The hackathon prize money was donated to the Libbitcoin project\'s future development.</p>',
            "skills": ["Bitcoin Protocol", "C / C++", "Shell Scripting", "Electronics"]
        },
        {
            "name": "Damian Cutillo",
            "img_path": "airbitz-theme/img-custom/portraits/damian.jpg",
            "title": "V.P. Design / Co-Founder",
            "nickname": "Web Geek",
            "bio_html": "<p>Damian has been involved with computer networking and system administration since 1999 and in 2006 he started building applications with open source internet technologies. Damian is a member of several open source communities and enjoys building things that are intuitive and beautiful in design and function. If it's a project that can help the planet evolve in a more balanced and harmonious way that promotes the evolution of consciousness then you can count Damian in.</p><p>In 2012, Damian co-founded Breadcrumbs, a mobile app to track your time and where you spend it. Breadcrumbs received awards at Uplinq 2012 conference, $50k in seed investment, and were accepted to the Qualcomm Labs EvoNexus startup incubator program in San Diego.</p><p>In April 2014 Damian teamed up with Amir Taaki, Pablo Martin, and William Swanson of the Libbitcoin and DarkWallet project in Toronto for the 2014 Bitcoin Expo Hackathon. The team won first place with the DarkMarket project, a proof of concept for one of the world's first fully decentralized, anonymous, peer to peer marketplaces. The hackathon prize money was donated to the Libbitcoin project's future development.</p>",
            "skills": ["Design / Development", "Django / WordPress", "UI/UX", "SEO / SEM"]
        },
        {
            "name": "Will Pangman",
            "img_path": "airbitz-theme/img-custom/portraits/will.jpg",
            "title": "Marketing Manager",
            "nickname": "Growth Maven",
            "bio_html": "<p>Will discovered Bitcoin in late 2012 and immediately engaged in building the human networks around this new technology. He founded Bitcoin Milwaukee, a 150+ volunteer community advocacy organization that quickly became known as one of the most active and successful Bitcoin outreach groups in North America. For the past year, he served as COO for the Bitcoin startup, Tapeke, and remains as an advisor to the company.</p><p>Before Bitcoin, Will worked as a production manager in the film and TV industry in New York City, and then as a marketing and business development consultant helping to update small businesses for the digital age. Will excels at relating the complexities of bitcoin to people of diverse backgrounds and awakening their curiosity to the power of distributed networks and stateless money.</p><p>Will has been a guest on many podcasts, frequently contributes to the World Crypto Network's flagship program The Bitcoin Group, and volunteers support to various standards and education projects in the space. Will brings his full sector knowledge, deep network, and relentless optimism to the Airbitz team, and looks forward to scaling the Airbitz tech stack to its first million users and beyond.</p>",
            "skills": ["User Engagement", "Public Speaking", "Social Networking", "Propaganda"]
        },
    ]

    team_info_row_2 = [
        {
            "name": "M.K. Lords",
            "img_path": "airbitz-theme/img-custom/portraits/mk.jpg",
            "title": "Marketing Manager",
            "nickname": "Strategy Ninja",
            "bio_html": "<p>M.K. Lords became interested in the disruptive and charitable potential of technology after being a writer for several years. She is best known as the editor of Bitcoin Not Bombs which was formed out of an alliance with Antiwar.com. Her focus has been on how block chain technology can help disadvantaged people and controversial organizations. She has written for Bitcoin Magazine, Bitcoin Not Bombs, been published in the educational book Bitcoin: At Issue, and featured in Forbes. M.K. also brings her experience from the financial services sector as the former office/media manager for Roberts & Roberts Brokerage.</p><p>While much of her work is written, she also has done extensive video interviews with prominent voices in the Bitcoin space. She has spoken on nonprofits, activism, and philosophy at tech and liberty themed conferences and also organized two Bitcoin conferences. She applies her experience in multiple fields as the Community Manager for Airbitz. When not writing and speaking, she fire dances and co-hosts the radio show Freedom Feens.</p>",
            "skills": ["Writing / Editing", "Public Speaking", "Content Creation", "Social Media Management"]
        },
        {
            "name": "Scott Morgan",
            "img_path": "airbitz-theme/img-custom/portraits/scott.jpg",
            "title": "H.R. Accounting / Co-Founder",
            "nickname": "Number Muncher",
            "bio_html": "<p>Scott has been on the finance side of the equation for most of his career. He has started several start ups and enjoys the excitement of building something new with a great team...and Airbitz is a great team!</p><p>Scott enjoys all things crypto and was bitten hard by the bug in 2012. He is excited to be in a space which can be created to help all individuals succeed in defining and achieving their own definition of success.</p>",
            "skills": ["California CPA", "Partnering & Networking", "Wallet User", "Ruby Newbie"]
        },
        {
            "name": "Nik Oraevkiy",
            "img_path": "airbitz-theme/img-custom/portraits/nik.jpg",
            "title": "Business Development / Analyst",
            "nickname": "Insight Escavator",
            "bio_html": "<p>Nik started trading various asset classes at the ripe old age of 14, quickly learning the fundamentals behind exchange operations and the value of independent research. He then continued to build out his skillset at the University of Waterloo, studying Economics and Finance, while actively participating in the FX and Equities markets.</p><p>Since graduating, Nik has started his own consulting/research firm that has been providing insights across a multitude of market segments, centering around technology, venture capital, gaming, and digital finance for the past 5 years. His multi-faceted analytical approach helped organizations shed new light on old problems, while at the same time prepared them for new ones.</p><p>While at Airbitz, Nik has used his long rooted trading knowledge and research skills to build a thorough understanding of how the new digital economy functions and has helped in strategically expanding the Airbitz vision into Canadian boarders.</p><p>In his off time, Nik is an avid freediver and back-country, hiker - he also enjoys crawling the vast reaches of the internet, absorbing information like a demosponge fresh from the BC coastal waters.</p>",
            "skills": ["Financial Analysis", "BI/CI/MI", "Deep Research", "Exchange Analysis"]
        },
        {
            "name": "\"RJ\" Raljoseph Ricasta",
            "img_path": "airbitz-theme/img-custom/portraits/rj.jpg",
            "title": "Lead Curator / QA",
            "nickname": "Bug Slayer",
            "bio_html": '<p>Mor on RJ soon.</p>',
            "skills": ["Quality Assurance", "Data Analysis", "Research", "Bitcoin Enthusiast"]
        },
        {
            "name": "Vincent Herrera",
            "img_path": "airbitz-theme/img-custom/portraits/vincent.jpg",
            "title": "Curator / QA",
            "nickname": "Data Wrapper",
            "bio_html": "<p>More on Vincent soon.</p>",
            "skills": ["Quality Assurance", "Data Visualization", "Finance", "Fieldwork"]
        },
        {
            "name": "Jacob Burrell",
            "img_path": "airbitz-theme/img-custom/portraits/jacob.jpg",
            "title": "Junior Developer / QA",
            "nickname": "Nitpicking Ninja",
            "bio_html": "<p>More on Jacob soon.</p>",
            "skills": ["Entrepreneur", "Quality Assurance", "Data Collection", "Scripting"]
        },
    ]

    context = {
        'active_regions': ACTIVE_REGIONS,
        'team_info_row_1': team_info_row_1,
        'team_info_row_2': team_info_row_2,
        'team_info': team_info_row_1 + team_info_row_2,
        # 'all_regions': ALL_REGIONS,
        # 'biz_total': Business.objects.filter(status="PUB", country__in=regions_data.get_active_country_codes()).count(),
    }
    return render_to_response('landing_v2.html', RequestContext(request, context))


def landing(request):
    print 'OLD LANDING'
    context = {
        'active_regions': ACTIVE_REGIONS,
        'all_regions': ALL_REGIONS,
        'biz_total': Business.objects.filter(status="PUB", country__in=regions_data.get_active_country_codes()).count(),
    }
    return render_to_response('home.html', RequestContext(request, context))

def __business_search__(request, action, arg_term=None, arg_category=None, arg_location=None, 
                        arg_ll=None, template='search.html'):
    if arg_term:
        term = arg_term
    else:
        term = request.GET.get('term', None)
    if arg_category:
        category = arg_category
    else:
        category = request.GET.get('category', None)
    if arg_ll:
        ll = arg_ll
    else:
        ll = request.GET.get('ll', None)
    if arg_location:
        location = arg_location
    else:
        location = request.GET.get('location', None)

    ip = api.getRequestIp(request)
    a = api.ApiProcess(locationStr=location, ll=ll, ip=ip)
    results = a.searchDirectory(term=term, category=category, show_hidden=False)

    if not results:
        return business_search_no_results(request, action) 

    request.session['nearText'] = location
    if location == 'On the Web':
        results_per_page = 30
    else:
        results_per_page = 25

    paginator = Paginator(results, results_per_page)

    page = request.GET.get('page')
    try:
        results = paginator.page(page)
        page_num = int(page)
    except PageNotAnInteger:
        page_num = 1
        results = paginator.page(page_num)
    except EmptyPage:
        page_num = paginator.num_pages
        results = paginator.page(page_num)

    results_left = min(paginator.count, results_per_page,
                       (paginator.count - results_per_page * (page_num - 1)))
    results_info = {
        'total': paginator.count,
        'results_left': results_left,
        'results_per_page': results_per_page
    }
    # populate missing fields from DB
    ids = []
    for r in results:
        ids.append(r.pk)
    bizs = dict([(str(b.pk), b) for b in Business.objects.filter(id__in=ids)])
    for r in results:
        biz = bizs[r.pk]
        r.has_bitcoin_discount = biz.has_bitcoin_discount
        r.get_absolute_url = biz.get_absolute_url()
        r.center = biz.center
        r.gmap_directions_url = biz.gmap_directions_url
        r.social = SocialId.objects.filter(business=biz)
        r.landing_image = biz.landing_image
        r.mobile_landing_image = biz.mobile_landing_image
        r.categories = biz.categories
        try:
            r.distance = calc_distance(a.userLocation(), biz.center)
        except Exception as e:
            print e

    context = {
        'search_action': action,
        'results': results,
        'mapkey': GOOGLE_MAP_KEY,
        'userLocation': a.userLocation(),
        'searchLocation': a.location,
        'was_search': True,
        'page_obj': paginator.page(page_num),
        'results_info': results_info,
        'form_action': '/blackfriday',

        # RELATED: REMOVING REGION MAP
        # 'active_regions': ACTIVE_REGIONS,
        # 'all_regions': ALL_REGIONS,
    }
    return render_to_response(template, RequestContext(request, context))

def business_search(request, *args, **kwargs):
    return __business_search__(request, reverse('search'), *args, **kwargs)

def blackfriday(request, **kwargs):
    kwargs['arg_category'] = SPECIALS_TAG
    kwargs['template'] = 'specials.html'
    return __business_search__(request, reverse('blackfriday'), **kwargs)


def business_search_no_results(request, action):
    context = {
        'search_action': action
    }
    return render_to_response('search-no-results.html', RequestContext(request, context))

def business_info(request, biz_id=None, biz_slug=None):

    biz = get_biz(request, pk=biz_id)

    if biz.status == 'PUB':
        if not biz_slug == biz.slug:
            return HttpResponsePermanentRedirect(biz.get_absolute_url())

    imgs = BusinessImage.objects.filter(business=biz)

    nearby = []
    if biz.center:
        nearby = Business.objects.filter(status='PUB').filter(\
                    ~Q(pk=biz.id), \
                    center__distance_lt=(biz.center, D(km=DISTANCE_LIMIT_KILOMETERS)))
        nearby = nearby.distance(biz.center).order_by('distance')[:12]
    context = {
        'biz': biz,
        'imgs': imgs,
        'results': nearby,
        'mapkey': GOOGLE_MAP_KEY,
        'biz_hours': get_biz_hours(biz),
        'weekdays': WEEKDAYS,
        'was_search': False,
    }
    return render_to_response('business_info.html', RequestContext(request, context))


def add_business(request, url=None):

    context = {
        'STATUS_CHOICES': STATUS_CHOICES,
        'SOCIAL_TYPES': SOCIAL_TYPES,
        'starter_url': url,
        'top_bg_img': '',
    }
    return render_to_response('business_add.html', RequestContext(request, context))




# handles email redirects for desktop or android gmail
def redirect_blf(request):

    address = request.GET['address']
    url = 'bitcoin:' + address
    # print '\n------------------------------------\n'
    # print 'ADDRESS:', address
    # print 'URL BUILT:', url
    # print '\n------------------------------------\n'
    response = HttpResponse("", status=302)
    response['Location'] = str(url)
    return response


def btc_email_request(request):
    context = {}
    return render_to_response('btc-email-request.html', RequestContext(request, context))

def email_request_template(request):
    context = {}
    return render_to_response('template-email-request.html', RequestContext(request, context))

def email_request_template_android(request):
    context = {}
    return render_to_response('template-email-request_android.html', RequestContext(request, context))


# app download fallback page
def app_download(request):
    return render_to_response('app-download.html')
