# used in template context processor 'active_regions'
def get_active_regions_list(region):
    regions = list()

    if region == 'SOUTHAMERICA':
        for region_code, data in ACTIVE_REGIONS_SOUTH_AMERICA.items():
            if '-' not in region_code:
                regions.append((data['name'], data['search']))
    if region == 'ASIA':
        for region_code, data in ACTIVE_REGIONS_ASIA.items():
            if '-' not in region_code:
                regions.append((data['name'], data['search']))
    if region == 'EU-':
        for region_code, data in ACTIVE_REGIONS_EUROPE.items():
            if '-' not in region_code:
                regions.append((data['name'], data['search']))
    else:
        for region_code, data in ACTIVE_REGIONS.items():
            if region in region_code:
                regions.append((data['name'], data['search']))

    regions.sort(key=lambda data: data[0])

    return regions


# ISO_3166 Region codes http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
# these correspond to jvectormaps

US_REGIONS = {
    'US-CA': {'name': 'California',
              'search': 'California, United States'},
    'US-TX': {'name': 'Texas',
              'search': 'Texas, United States'},
    'US-NY': {'name': 'New York',
              'search': 'New York, United States'},
    'US-HI': {'name': 'Hawaii',
              'search': 'Hawaii, United States'},
    'US-NJ': {'name': 'New Jersey',
              'search': 'New Jersey, United States'},
    'US-GA': {'name': 'Georgia',
              'search': 'Georgia, United States'},
    'US-IL': {'name': 'Illinois',
              'search': 'Illinois, United States'},
    'US-UT': {'name': 'Utah',
              'search': 'Utah, United States'},
    'US-NV': {'name': 'Nevada',
              'search': 'Nevada, United States'},
    'US-CO': {'name': 'Colorado',
              'search': 'Colorado, United States'},
    'US-FL': {'name': 'Florida',
              'search': 'Florida, United States'},
    'US-NH': {'name': 'New Hampshire',
              'search': 'New Hapshire, United States'},
    'US-MA': {'name': 'Massachusetts',
              'search': 'Massachusetts, United States'},
    'US-VT': {'name': 'Vermont',
              'search': 'Vermont, United States'},
    'US-PA': {'name': 'Pennsylvania',
              'search': 'Pennsylvania, United States'},
    'US-CT': {'name': 'Connecticut',
              'search': 'Connecticut, United States'},
    'US-DE': {'name': 'Delaware',
              'search': 'Delaware, United States'},
    'US-MD': {'name': 'Maryland',
              'search': 'Maryland, United States'},
    'US-ME': {'name': 'Maine',
              'search': 'Maine, United States'},
    'US-WA': {'name': 'Washington',
              'search': 'Washington, United States'},
    'US-OR': {'name': 'Oregon',
              'search': 'Oregon, United States'},
    'US-AK': {'name': 'Alaska',
              'search': 'Alaska, United States'},
    'US-AZ': {'name': 'Arizona',
              'search': 'Arizona, United States'},
    'US-NM': {'name': 'New Mexico',
              'search': 'New Mexico, United States'},
    'US-MI': {'name': 'Michigan',
              'search': 'Michigan, United States'},
    'US-MN': {'name': 'Minnesota',
              'search': 'Minnesota, United States'},
    'US-DC': {'name': 'Washington DC',
              'search': 'Washington, DC, United States'},
    'US-IN': {'name': 'Indiana',
              'search': 'Indiana, United States'},
    'US-IA': {'name': 'Iowa',
              'search': 'Iowa, United States'},
    'US-KS': {'name': 'Kansas',
              'search': 'Kansas, United States'},
    'US-WY': {'name': 'Wyoming',
              'search': 'Wyoming, United States'},
    'US-MT': {'name': 'Montana',
              'search': 'Montana, United States'},
    'US-ID': {'name': 'Idaho',
              'search': 'Idaho, United States'},
    'US-ND': {'name': 'North Dakota',
              'search': 'North Dakota, United States'},
    'US-SD': {'name': 'South Dakota',
              'search': 'South Dakota, United States'},
    'US-NE': {'name': 'Nebraska',
              'search': 'Nebraska, United States'},
    'US-MO': {'name': 'Missouri',
              'search': 'Missouri, United States'},
    'US-OK': {'name': 'Oklahoma',
              'search': 'Oklahoma, United States'},
    'US-AR': {'name': 'Arkansas',
              'search': 'Arkansas, United States'},
    'US-LA': {'name': 'Louisiana',
              'search': 'Louisiana, United States'},
    'US-MS': {'name': 'Mississippi',
              'search': 'Mississippi, United States'},
    'US-AL': {'name': 'Alabama',
              'search': 'Alabama, United States'},
    'US-TN': {'name': 'Tennessee',
              'search': 'Tennessee, United States'},
    'US-KY': {'name': 'Kentucky',
              'search': 'Kentucky, United States'},
    'US-OH': {'name': 'Ohio',
              'search': 'Ohio, United States'},
    'US-WV': {'name': 'West Virginia',
              'search': 'West Virginia, United States'},
    'US-VA': {'name': 'Virginia',
              'search': 'Virginia, United States'},
    'US-NC': {'name': 'North Carolina',
              'search': 'North Carolina, United States'},
    'US-SC': {'name': 'South Carolina',
              'search': 'South Carolina, United States'},
    'US-WI': {'name': 'Wisconsin',
              'search': 'Wisconsin, United States'},
}

CA_REGIONS = {
    'CA-ON': {'name': 'Ontario',
              'search': 'Ontario, Canada'},
    'CA-BC': {'name': 'British Columbia',
              'search': 'Ontario, Canada'},
    'CA-QC': {'name': 'Quebec',
              'search': 'Quebec, Canada'},
    'CA-YT': {'name': 'Yukon',
              'search': 'Yukon, Canada'},
    'CA-NT': {'name': 'Northwest Territories',
              'search': 'Northwest Territories, Canada'},
    'CA-NU': {'name': 'Nunavut',
              'search': 'Nunavut, Canada'},
    'CA-AB': {'name': 'Alberta',
              'search': 'Alberta, Canada'},
    'CA-SK': {'name': 'Saskatchewan',
              'search': 'Saskatchewan, Canada'},
    'CA-MB': {'name': 'Manitoba',
              'search': 'Manitoba, Canada'},
    'CA-NL': {'name': 'Newfoundland and Labrador',
              'search': 'Newfoundland and Labrador, Canada'},
    'CA-NB': {'name': 'New Brunswick',
              'search': 'New Brunswick, Canada'},
    'CA-NS': {'name': 'Nova Scotia',
              'search': 'Nova Scotia, Canada'},
    'CA-PE': {'name': 'Prince Edward Island',
              'search': 'Prince Edward Island, Canada'},
}

EU_REGIONS = {
    'NL': {'name': 'Netherlands',
           'search': 'Netherlands'},
    'IS': {'name': 'Iceland',
       'search': 'Iceland'},
    'GB': {'name': 'United Kingdom',
       'search': 'United Kingdom'},
    'IE': {'name': 'Ireland',
       'search': 'Ireland'},
    'NO': {'name': 'Norway',
       'search': 'Norway'},
    'SE': {'name': 'Sweden',
       'search': 'Sweden'},
    'FI': {'name': 'Finland',
       'search': 'Finland'},
    'RU': {'name': 'Russia',
       'search': 'Russia'},
    'EE': {'name': 'Estonia',
       'search': 'Estonia'},
    'LV': {'name': 'Latvia',
       'search': 'Latvia'},
    'BY': {'name': 'Belarus',
       'search': 'Belarus'},
    'UA': {'name': 'Ukraine',
       'search': 'Ukraine'},
    'LT': {'name': 'Lithuania',
       'search': 'Lithuania'},
    'MD': {'name': 'Moldova',
       'search': 'Moldova'},
    'RO': {'name': 'Romania',
       'search': 'Romania'},
    'BG': {'name': 'Bulgaria',
       'search': 'Bulgaria'},
    'TR': {'name': 'Turkey',
       'search': 'Turkey'},
    'GR': {'name': 'Greece',
       'search': 'Greece'},
    'AL': {'name': 'Albania',
       'search': 'Albania'},
    'MK': {'name': 'Macedonia',
       'search': 'Macedonia'},
    'RS': {'name': 'Republic of Serbia',
       'search': 'Republic of Serbia'},
    'SK': {'name': 'Slovakia',
       'search': 'Slovakia'},
    'PL': {'name': 'Poland',
       'search': 'Poland'},
    'DE': {'name': 'Germany',
       'search': 'Germany'},
    'CZ': {'name': 'Czech Republic',
       'search': 'Czech Republic'},
    'AT': {'name': 'Austria',
       'search': 'Austria'},
    'HR': {'name': 'Croatia',
       'search': 'Croatia'},
    'BA': {'name': 'Bosnia and Herzegovina',
       'search': 'Bosnia and Herzegovina'},
    'ME': {'name': 'Montenegro',
       'search': 'Montenegro'},
    'BE': {'name': 'Belgium',
       'search': 'Belgium'},
    'FR': {'name': 'France',
       'search': 'France'},
    'IT': {'name': 'Italy',
       'search': 'Italy'},
    'CH': {'name': 'Switzerland',
       'search': 'Switzerland'},
    'ES': {'name': 'Spain',
       'search': 'Spain'},
    'PT': {'name': 'Portugal',
       'search': 'Portugal'},
    'SY': {'name': 'Syria',
       'search': 'Syria'},
    'IQ': {'name': 'Iraq',
       'search': 'Iraq'},
    'LB': {'name': 'Lebanon',
       'search': 'Lebanon'},
    'IL': {'name': 'Israel',
       'search': 'Israel'},
    'JO': {'name': 'Jordan',
       'search': 'Jordan'},
    'SA': {'name': 'Saudi Arabia',
       'search': 'Saudi Arabia'},
    'EG': {'name': 'Egypt',
       'search': 'Egypt'},
    'LY': {'name': 'Libya',
       'search': 'Libya'},
    'DZ': {'name': 'Algeria',
       'search': 'Algeria'},
    'TN': {'name': 'Tanzania',
       'search': 'Tanzania'},
    'MA': {'name': 'Morocco',
       'search': 'Morocco'},
    'PS': {'name': 'West Bank',
       'search': 'West Bank'},
    'SI': {'name': 'Slovenia',
       'search': 'Slovenia'},
    '2': {'name': 'Kosovo',
       'search': 'Kosovo'},
    'LU': {'name': 'Luxembourg',
       'search': 'Luxembourg'},
    'LI': {'name': 'Liechenstein',
       'search': 'Liechenstein'},
}

SOUTH_AMERICA_REGIONS = {}  # TODO: get full list

ASIA_REGIONS = {}           # TODO: get full list

# Regions listed with partial coverage listed below
ACTIVE_REGIONS_EUROPE = {
    # EU regions
    'NL': {'name': 'Netherlands',
           'search': 'Netherlands'},
    'GB': {'name': 'United Kingdom',
           'search': 'United Kingdom'},
    'DE': {'name': 'Germany',
           'search': 'Germany'},
    'AT': {'name': 'Austria',
           'search': 'Austria'},
}

ACTIVE_REGIONS_SOUTH_AMERICA = {
    # South American regions
    'BR': {'name': 'Brazil',
           'search': 'Brazil'},
}

ACTIVE_REGIONS_ASIA = {
    # Asian regions
    'HK': {'name': 'Hong Kong',
           'search': 'Hong Kong'},
}

ACTIVE_REGIONS = {}
ACTIVE_REGIONS.update(US_REGIONS)   # all
ACTIVE_REGIONS.update(CA_REGIONS)   # all
ACTIVE_REGIONS.update(ACTIVE_REGIONS_EUROPE)            # partial
ACTIVE_REGIONS.update(ACTIVE_REGIONS_ASIA)              # partial
ACTIVE_REGIONS.update(ACTIVE_REGIONS_SOUTH_AMERICA)     # partial

# ALL_REGIONS = dict(US_REGIONS.items() + CA_REGIONS.items() + EU_REGIONS.items())
ALL_REGIONS = {}
ALL_REGIONS.update(US_REGIONS)
ALL_REGIONS.update(CA_REGIONS)
ALL_REGIONS.update(EU_REGIONS)
