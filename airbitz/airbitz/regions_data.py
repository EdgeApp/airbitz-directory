from airbitz.region_definitions import *


# used in restapi endpoints
def get_active_country_codes():
    c_codes = list()

    for country_code, data in ACTIVE_REGIONS.items():
        c_codes.append(country_code[:2])

    return list(set(c_codes))  # return distinct list of c_codes


# used in template context processor 'active_regions'
def get_active_regions_list(region):
    regions = list()

    if region == 'SOUTHAMERICA':
        for region_code, data in ACTIVE_REGIONS_SOUTH_AMERICA.items():
            if '-' not in region_code:
                regions.append((data['name'], data['search']))
    elif region == 'ASIA':
        for region_code, data in ACTIVE_REGIONS_ASIA.items():
            if '-' not in region_code:
                regions.append((data['name'], data['search']))
    elif region == 'SOUTHEAST_ASIA':
        for region_code, data in ACTIVE_REGIONS_SOUTHEAST_ASIA.items():
            if '-' not in region_code:
                regions.append((data['name'], data['search']))
    elif region == 'EUROPE':
        for region_code, data in ACTIVE_REGIONS_EUROPE.items():
            if '-' not in region_code:
                regions.append((data['name'], data['search']))
    elif region == 'OCEANA':
        for region_code, data in ACTIVE_REGIONS_OCEANA.items():
            if '-' not in region_code:
                regions.append((data['name'], data['search']))
    else:
        for region_code, data in ACTIVE_REGIONS.items():
            if region in region_code:
                regions.append((data['name'], data['search']))

    regions.sort(key=lambda data: data[0])

    return regions


# Regions listed with partial coverage listed below
ACTIVE_REGIONS_EUROPE = {
    # EU regions
    'NL': {'name': 'Netherlands',
           'search': 'Netherlands'},
    'UK': {'name': 'United Kingdom',
           'search': 'United Kingdom'},
    'DE': {'name': 'Germany',
           'search': 'Germany'},
    'AT': {'name': 'Austria',
           'search': 'Austria'},
    'CH': {'name': 'Switzerland',
           'search': 'Switzerland'},
    'IE': {'name': 'Ireland',
           'search': 'Ireland'},

}

ACTIVE_REGIONS_SOUTH_AMERICA = {
    # South American regions
    'BR': {'name': 'Brazil',
           'search': 'Brazil'},
    'AR': {'name': 'Argentina',
           'search': 'Argentina'},
}

ACTIVE_REGIONS_ASIA = {
    # Asian regions
    'HK': {'name': 'Hong Kong',
           'search': 'Hong Kong'},
}

ACTIVE_REGIONS_SOUTHEAST_ASIA = {
    # Southeast Asian regions
    'PH': {'name': 'Philippines',
           'search': 'Philippines'},
}

ACTIVE_REGIONS_OCEANA = {
    # Oceana regions
    'AU': {'name': 'Australia',
           'search': 'Australia'},
    'NZ': {'name': 'New Zealand',
           'search': 'New Zealand'},
}

ACTIVE_REGIONS = {}
ACTIVE_REGIONS.update(US_REGIONS)   # all
ACTIVE_REGIONS.update(CA_REGIONS)   # all
ACTIVE_REGIONS.update(ACTIVE_REGIONS_EUROPE)            # partial
ACTIVE_REGIONS.update(ACTIVE_REGIONS_ASIA)              # partial
ACTIVE_REGIONS.update(ACTIVE_REGIONS_SOUTHEAST_ASIA)    # partial
ACTIVE_REGIONS.update(ACTIVE_REGIONS_SOUTH_AMERICA)     # partial
ACTIVE_REGIONS.update(ACTIVE_REGIONS_OCEANA)        # partial

ALL_REGIONS = {}
ALL_REGIONS.update(US_REGIONS)
ALL_REGIONS.update(CA_REGIONS)
ALL_REGIONS.update(EU_REGIONS)

