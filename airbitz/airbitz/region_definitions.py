# static file with region codes until we move to db model for it


# ISO_3166 Region codes http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
ALL_COUNTRY_LABELS = {
    "AD": "Andorra",
    "AE": "United Arab Emirates",
    "AF": "Afghanistan",
    "AG": "Antigua and Barbuda",
    "AI": "Anguilla",
    "AL": "Albania",
    "AM": "Armenia",
    "AO": "Angola",
    "AQ": "Antarctica",
    "AR": "Argentina",
    "AS": "American Samoa",
    "AT": "Austria",
    "AU": "Australia",
    "AW": "Aruba",
    "AX": "Aland Islands",
    "AZ": "Azerbaijan",
    "BA": "Bosnia and Herzegovina",
    "BB": "Barbados",
    "BD": "Bangladesh",
    "BE": "Belgium",
    "BF": "Burkina Faso",
    "BG": "Bulgaria",
    "BH": "Bahrain",
    "BI": "Burundi",
    "BJ": "Benin",
    "BL": "Saint Barthelemy",
    "BM": "Bermuda",
    "BN": "Brunei Darussalam",
    "BO": "Bolivia, Plurinational State of",
    "BQ": "Bonaire, Sint Eustatius and Saba",
    "BR": "Brazil",
    "BS": "Bahamas",
    "BT": "Bhutan",
    "BV": "Bouvet Island",
    "BW": "Botswana",
    "BY": "Belarus",
    "BZ": "Belize",
    "CA": "Canada",
    "CC": "Cocos (Keeling) Islands",
    "CD": "Congo, the Democratic Republic of the",
    "CF": "Central African Republic",
    "CG": "Congo",
    "CH": "Switzerland",
    "CI": "Cote d'Ivoire",
    "CK": "Cook Islands",
    "CL": "Chile",
    "CM": "Cameroon",
    "CN": "China",
    "CO": "Colombia",
    "CR": "Costa Rica",
    "CU": "Cuba",
    "CV": "Cabo Verde",
    "CW": "Curacao",
    "CX": "Christmas Island",
    "CY": "Cyprus",
    "CZ": "Czech Republic",
    "DE": "Germany",
    "DJ": "Djibouti",
    "DK": "Denmark",
    "DM": "Dominica",
    "DO": "Dominican Republic",
    "DZ": "Algeria",
    "EC": "Ecuador",
    "EE": "Estonia",
    "EG": "Egypt",
    "EH": "Western Sahara",
    "ER": "Eritrea",
    "ES": "Spain",
    "ET": "Ethiopia",
    "FI": "Finland",
    "FJ": "Fiji",
    "FK": "Falkland Islands (Malvinas)",
    "FM": "Micronesia, Federated States of",
    "FO": "Faroe Islands",
    "FR": "France",
    "GA": "Gabon",
    "GB": "United Kingdom",
    "GD": "Grenada",
    "GE": "Georgia",
    "GF": "French Guiana",
    "GG": "Guernsey",
    "GH": "Ghana",
    "GI": "Gibraltar",
    "GL": "Greenland",
    "GM": "Gambia",
    "GN": "Guinea",
    "GP": "Guadeloupe",
    "GQ": "Equatorial Guinea",
    "GR": "Greece",
    "GS": "South Georgia and the South Sandwich Islands",
    "GT": "Guatemala",
    "GU": "Guam",
    "GW": "Guinea-Bissau",
    "GY": "Guyana",
    "HK": "Hong Kong",
    "HM": "Heard Island and McDonald Islands",
    "HN": "Honduras",
    "HR": "Croatia",
    "HT": "Haiti",
    "HU": "Hungary",
    "ID": "Indonesia",
    "IE": "Ireland",
    "IL": "Israel",
    "IM": "Isle of Man",
    "IN": "India",
    "IO": "British Indian Ocean Territory",
    "IQ": "Iraq",
    "IR": "Iran, Islamic Republic of",
    "IS": "Iceland",
    "IT": "Italy",
    "JE": "Jersey",
    "JM": "Jamaica",
    "JO": "Jordan",
    "JP": "Japan",
    "KE": "Kenya",
    "KG": "Kyrgyzstan",
    "KH": "Cambodia",
    "KI": "Kiribati",
    "KM": "Comoros",
    "KN": "Saint Kitts and Nevis",
    "KP": "Korea, Democratic People's Republic of",
    "KR": "Korea, Republic of",
    "KW": "Kuwait",
    "KY": "Cayman Islands",
    "KZ": "Kazakhstan",
    "LA": "Lao People's Democratic Republic",
    "LB": "Lebanon",
    "LC": "Saint Lucia",
    "LI": "Liechtenstein",
    "LK": "Sri Lanka",
    "LR": "Liberia",
    "LS": "Lesotho",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "LV": "Latvia",
    "LY": "Libya",
    "MA": "Morocco",
    "MC": "Monaco",
    "MD": "Moldova, Republic of",
    "ME": "Montenegro",
    "MF": "Saint Martin (French part)",
    "MG": "Madagascar",
    "MH": "Marshall Islands",
    "MK": "Macedonia, the former Yugoslav Republic of",
    "ML": "Mali",
    "MM": "Myanmar",
    "MN": "Mongolia",
    "MO": "Macao",
    "MP": "Northern Mariana Islands",
    "MQ": "Martinique",
    "MR": "Mauritania",
    "MS": "Montserrat",
    "MT": "Malta",
    "MU": "Mauritius",
    "MV": "Maldives",
    "MW": "Malawi",
    "MX": "Mexico",
    "MY": "Malaysia",
    "MZ": "Mozambique",
    "NA": "Namibia",
    "NC": "New Caledonia",
    "NE": "Niger",
    "NF": "Norfolk Island",
    "NG": "Nigeria",
    "NI": "Nicaragua",
    "NL": "Netherlands",
    "NO": "Norway",
    "NP": "Nepal",
    "NR": "Nauru",
    "NU": "Niue",
    "NZ": "New Zealand",
    "OM": "Oman",
    "PA": "Panama",
    "PE": "Peru",
    "PF": "French Polynesia",
    "PG": "Papua New Guinea",
    "PH": "Philippines",
    "PK": "Pakistan",
    "PL": "Poland",
    "PM": "Saint Pierre and Miquelon",
    "PN": "Pitcairn",
    "PR": "Puerto Rico",
    "PS": "Palestine, State of",
    "PT": "Portugal",
    "PW": "Palau",
    "PY": "Paraguay",
    "QA": "Qatar",
    "RE": "Reunion",
    "RO": "Romania",
    "RS": "Serbia",
    "RU": "Russian Federation",
    "RW": "Rwanda",
    "SA": "Saudi Arabia",
    "SB": "Solomon Islands",
    "SC": "Seychelles",
    "SD": "Sudan",
    "SE": "Sweden",
    "SG": "Singapore",
    "SH": "Saint Helena, Ascension and Tristan da Cunha",
    "SI": "Slovenia",
    "SJ": "Svalbard and Jan Mayen",
    "SK": "Slovakia",
    "SL": "Sierra Leone",
    "SM": "San Marino",
    "SN": "Senegal",
    "SO": "Somalia",
    "SR": "Suriname",
    "SS": "South Sudan",
    "ST": "Sao Tome and Principe",
    "SV": "El Salvador",
    "SX": "Sint Maarten (Dutch part)",
    "SY": "Syrian Arab Republic",
    "SZ": "Swaziland",
    "TC": "Turks and Caicos Islands",
    "TD": "Chad",
    "TF": "French Southern Territories",
    "TG": "Togo",
    "TH": "Thailand",
    "TJ": "Tajikistan",
    "TK": "Tokelau",
    "TL": "Timor-Leste",
    "TM": "Turkmenistan",
    "TN": "Tunisia",
    "TO": "Tonga",
    "TR": "Turkey",
    "TT": "Trinidad and Tobago",
    "TV": "Tuvalu",
    "TW": "Taiwan, Province of China",
    "TZ": "Tanzania, United Republic of",
    "UA": "Ukraine",
    "UG": "Uganda",
    "UM": "United States Minor Outlying Islands",
    "US": "United States",
    "UY": "Uruguay",
    "UZ": "Uzbekistan",
    "VA": "Holy See (Vatican City State)",
    "VC": "Saint Vincent and the Grenadines",
    "VE": "Venezuela, Bolivarian Republic of",
    "VG": "Virgin Islands, British",
    "VI": "Virgin Islands, U.S.",
    "VN": "Viet Nam",
    "VU": "Vanuatu",
    "WF": "Wallis and Futuna",
    "WS": "Samoa",
    "YE": "Yemen",
    "YT": "Mayotte",
    "ZA": "South Africa",
    "ZM": "Zambia",
    "ZW": "Zimbabwe"
}

# subregions of countries
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
    'US-RI': {'name': 'Rhode Island',
              'search': 'Rhode Island, United States'},
    'US-PR': {'name': 'Puerto Rico',
              'search': 'Puerto Rico, United States'},
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

AU_REGIONS = {
    'AU-VIC': {'name': 'Victoria',
               'search': 'Victoria, Australia'},
    'AU-NSW': {'name': 'New South Wales',
               'search': 'New South Wales, Australia'},
    'AU-QLD': {'name': 'Queensland',
               'search': 'Queensland, Australia'},
    'AU-WA': {'name': 'Western Australia',
              'search': 'Western Australia, Australia'},
    'AU-ACT': {'name': 'Australian Capital Territory',
               'search': 'Australian Capital Territory, Australia'},
    'AU-SA': {'name': 'South Australia',
              'search': 'South Australia, Australia'},
    'AU-TAS': {'name': 'Tasmania',
               'search': 'Tasmania, Australia'},
}

DE_REGIONS = {
    'DE-BW': {'name': 'Baden-Wurttemberg',
              'search': 'Baden-Wurttemberg, Germany'},
    'DE-BY': {'name': 'Bavaria',
              'search': 'Bavaria, Germany'},
    'DE-BE': {'name': 'Berlin',
              'search': 'Berlin, Germany'},
    'DE-BB': {'name': 'Brandenburg',
              'search': 'Brandenburg, Germany'},
    'DE-HB': {'name': 'Bremen',
              'search': 'Bremen, Germany'},
    'DE-HH': {'name': 'Hamburg',
              'search': 'Hamburg, Germany'},
    'DE-HE': {'name': 'Hesse',
              'search': 'Hesse, Germany'},
    'DE-NI': {'name': 'Lower Saxony',
              'search': 'Lower Saxony, Germany'},
    'DE-MV': {'name': 'Mecklenburg-Vorpommern',
              'search': 'Mecklenburg-Vorpommern, Germany'},
    'DE-NW': {'name': 'North Rhine-Westphalia',
              'search': 'North Rhine-Westphalia, Germany'},
    'DE-RP': {'name': 'Rhineland-Palatinate',
              'search': 'Rhineland-Palatinate, Germany'},
    'DE-SL': {'name': 'Saarland',
              'search': 'Saarland, Germany'},
    'DE-SN': {'name': 'Saxony',
              'search': 'Saxony, Germany'},
    'DE-ST': {'name': 'Saxony-Anhalt',
              'search': 'Saxony-Anhalt, Germany'},
    'DE-SH': {'name': 'Schleswig-Holstein',
              'search': 'Schleswig-Holstein, Germany'},
    'DE-TH': {'name': 'Thuringia',
              'search': 'Thuringia, Germany'},
}

NL_REGIONS = {
    'NL-DR': {'name': 'Drenthe',
              'search': 'Drenthe, Netherlands'},
    'NL-FL': {'name': 'Flevoland',
              'search': 'Flevoland, Netherlands'},
    'NL-FR': {'name': 'Fryslan',
              'search': 'Fryslan, Netherlands'},
    'NL-GE': {'name': 'Gelderland',
              'search': 'Gelderland, Netherlands'},
    'NL-GR': {'name': 'Groningen',
              'search': 'Groningen, Netherlands'},
    'NL-LI': {'name': 'Limburg',
              'search': 'Limburg, Netherlands'},
    'NL-NB': {'name': 'North Brabant',
              'search': 'North Brabant, Netherlands'},
    'NL-NH': {'name': 'North Holland',
              'search': 'North Holland, Netherlands'},
    'NL-OV': {'name': 'Overijssel',
              'search': 'Overijssel, Netherlands'},
    'NL-UT': {'name': 'Utrecht',
              'search': 'Utrecht, Netherlands'},
    'NL-ZE': {'name': 'Zeeland',
              'search': 'Zeeland, Netherlands'},
    'NL-ZH': {'name': 'South Holland',
              'search': 'South Holland, Netherlands'},
}

AR_REGIONS = {
    'AR-CF': {'name': 'Buenos Arires City',
              'search': 'Buenos Arires City, Argentina'},
    'AR-BA': {'name': 'Buenos Arires',
              'search': 'Buenos Arire, Argentina'},
    'AR-CT': {'name': 'Catamarca',
              'search': 'Catamarca, Argentina'},
    'AR-CC': {'name': 'Chaco',
              'search': 'Chaco, Argentina'},
    'AR-CH': {'name': 'Chubut',
              'search': 'Chubut, Argentina'},
    'AR-CD': {'name': 'Cordoba',
              'search': 'Cordoba, Argentina'},
    'AR-CR': {'name': 'Corrientes',
              'search': 'Corrientes, Argentina'},
    'AR-ER': {'name': 'Entre Rios',
              'search': 'Entre Rios, Argentina'},
    'AR-FO': {'name': 'Formosa',
              'search': 'Formosa, Argentina'},
    'AR-JY': {'name': 'Jujuy',
              'search': 'Jujuy, Argentina'},
    'AR-LP': {'name': 'La Pampa',
              'search': 'La Pampa, Argentina'},
    'AR-LR': {'name': 'La Rioja',
              'search': 'La Rioja, Argentina'},
    'AR-MZ': {'name': 'Mendoza',
              'search': 'Mendoza, Argentina'},
    'AR-MN': {'name': 'Misiones',
              'search': 'Misiones, Argentina'},
    'AR-NQ': {'name': 'Neuquen',
              'search': 'Neuquen, Argentina'},
    'AR-RN': {'name': 'Rio Negro',
              'search': 'Rio Negro, Argentina'},
    'AR-SA': {'name': 'Salta',
              'search': 'Salta, Argentina'},
    'AR-SJ': {'name': 'San Juan',
              'search': 'San Juan, Argentina'},
    'AR-SL': {'name': 'San Luis',
              'search': 'San Luis, Argentina'},
    'AR-SC': {'name': 'Santa Cruz',
              'search': 'Santa Cruz, Argentina'},
    'AR-SF': {'name': 'Santa Fe',
              'search': 'Santa Fe, Argentina'},
    'AR-SE': {'name': 'Santiago del Estero',
              'search': 'Santiago del Estero, Argentina'},
    'AR-TF': {'name': 'Tierra del Fuego',
              'search': 'Tierra del Fuego, Argentina'},
    'AR-TM': {'name': 'Tucuman',
              'search': 'Tucuman, Argentina'},
}

BR_REGIONS = {
    'BR-AC': {'name': 'Acre',
              'search': 'Acre, Brazil'},
    'BR-AL': {'name': 'Alagoas',
              'search': 'Alagoas, Brazil'},
    'BR-AP': {'name': 'Amapa',
              'search': 'Amapa, Brazil'},
    'BR-AM': {'name': 'Amazonas',
              'search': 'Amazonas, Brazil'},
    'BR-BA': {'name': 'Bahia',
              'search': 'Bahia, Brazil'},
    'BR-CE': {'name': 'Ceara',
              'search': 'Ceara, Brazil'},
    'BR-DF': {'name': 'Distrito Federal',
              'search': 'Distrito Federal, Brazil'},
    'BR-ES': {'name': 'Espirito Santo',
              'search': 'Espirito Santo, Brazil'},
    'BR-GO': {'name': 'Goias',
              'search': 'Goias, Brazil'},
    'BR-MA': {'name': 'Maranhao',
              'search': 'Maranhao, Brazil'},
    'BR-MT': {'name': 'Mato Grosso',
              'search': 'Mato Grosso, Brazil'},
    'BR-MS': {'name': 'Mato Grosso do Sul',
              'search': 'Mato Grosso do Sul, Brazil'},
    'BR-MG': {'name': 'Minas Gerais',
              'search': 'Minas Gerais, Brazil'},
    'BR-PA': {'name': 'Para',
              'search': 'Para, Brazil'},
    'BR-PB': {'name': 'Paraiba',
              'search': 'Paraiba, Brazil'},
    'BR-PR': {'name': 'Parana',
              'search': 'Parana, Brazil'},
    'BR-PE': {'name': 'Pernambuco',
              'search': 'Pernambuco, Brazil'},
    'BR-PI': {'name': 'Piaui',
              'search': 'Piaui, Brazil'},
    'BR-RJ': {'name': 'Rio de Janeiro',
              'search': 'Rio de Janeiro, Brazil'},
    'BR-RN': {'name': 'Rio Grande do Norte',
              'search': 'Rio Grande do Norte, Brazil'},
    'BR-RS': {'name': 'Rio Grande do Sul',
              'search': 'Rio Grande do Sul, Brazil'},
    'BR-RO': {'name': 'Rondonia',
              'search': 'Rondonia, Brazil'},
    'BR-RR': {'name': 'Roraima',
              'search': 'Roraima, Brazil'},
    'BR-SC': {'name': 'Santa Catarina',
              'search': 'Santa Catarina, Brazil'},
    'BR-SP': {'name': 'Sao Paulo',
              'search': 'Sao Paulo, Brazil'},
    'BR-SE': {'name': 'Sergipe',
              'search': 'Sergipe, Brazil'},
    'BR-TO': {'name': 'Tocantins',
              'search': 'Tocantins, Brazil'},
}

CH_REGIONS = {
    'CH-AG': {'name': 'Aargau',
              'search': 'Aargau, Switzerland'},
    'CH-AI': {'name': 'Appenzell Innerrhoden',
              'search': 'Appenzell Innerrhoden, Switzerland'},
    'CH-AR': {'name': 'Appenzell Ausserrhoden',
              'search': 'Appenzell Ausserrhoden, Switzerland'},
    'CH-BE': {'name': 'Bern',
              'search': 'Bern, Switzerland'},
    'CH-BL': {'name': 'Basel-Landschaft',
              'search': 'Basel-Landschaft, Switzerland'},
    'CH-BS': {'name': 'Basel-Stadt',
              'search': 'Basel-Stadt, Switzerland'},
    'CH-FR': {'name': 'Fribourg',
              'search': 'Fribourg, Switzerland'},
    'CH-GE': {'name': 'Geneva',
              'search': 'Geneva, Switzerland'},
    'CH-GL': {'name': 'Glarus',
              'search': 'Glarus, Switzerland'},
    'CH-GR': {'name': 'Graubunden',
              'search': 'Graubunden, Switzerland'},
    'CH-JU': {'name': 'Jura',
              'search': 'Jura, Switzerland'},
    'CH-LU': {'name': 'Lucerne',
              'search': 'Lucerne, Switzerland'},
    'CH-NE': {'name': 'Neuchatel',
              'search': 'Neuchatel, Switzerland'},
    'CH-NW': {'name': 'Nidwalden',
              'search': 'Nidwalden, Switzerland'},
    'CH-OW': {'name': 'Obwalden',
              'search': 'Obwalden, Switzerland'},
    'CH-SG': {'name': 'St. Gallen',
              'search': 'St. Gallen, Switzerland'},
    'CH-SH': {'name': 'Schaffhausen',
              'search': 'Schaffhausen, Switzerland'},
    'CH-SO': {'name': 'Solothurn',
              'search': 'Solothurn, Switzerland'},
    'CH-SZ': {'name': 'Schwyz',
              'search': 'Schwyz, Switzerland'},
    'CH-TG': {'name': 'Thurgau',
              'search': 'Thurgau, Switzerland'},
    'CH-TI': {'name': 'Ticino',
              'search': 'Ticino, Switzerland'},
    'CH-UR': {'name': 'Uri',
              'search': 'Uri, Switzerland'},
    'CH-VD': {'name': 'Vaud',
              'search': 'Vaud, Switzerland'},
    'CH-VS': {'name': 'Valais',
              'search': 'Valais, Switzerland'},
    'CH-ZG': {'name': 'Zug',
              'search': 'Zug, Switzerland'},
    'CH-ZH': {'name': 'Zurich',
              'search': 'Zurich, Switzerland'},
}

AT_REGIONS = {
    'AT-BU': {'name': 'Burgenland',
              'search': 'Burgenland, Austria'},
    'AT-KA': {'name': 'Carinthia',
              'search': 'Carinthia, Austria'},
    'AT-NO': {'name': 'Lower Austria',
              'search': 'Lower Austria, Austria'},
    'AT-SZ': {'name': 'Salzburg',
              'search': 'Salzburg, Austria'},
    'AT-ST': {'name': 'Styria',
              'search': 'Styria, Austria'},
    'AT-TR': {'name': 'Tyrol',
              'search': 'Tyrol, Austria'},
    'AT-OO': {'name': 'Upper Austria',
              'search': 'Upper Austria, Austria'},
    'AT-WI': {'name': 'Vienna',
              'search': 'Vienna, Austria'},
    'AT-VO': {'name': 'Vorarlberg',
              'search': 'Vorarlberg, Austria'},
}

NZ_REGIONS = {
    'NZ-AU': {'name': 'Auckland',
              'search': 'Auckland, New Zealand'},
    'NZ-BP': {'name': 'Bay of Plenty',
              'search': 'Bay of Plenty, New Zealand'},
    'NZ-CA': {'name': 'Canterbury',
              'search': 'Canterbury, New Zealand'},
    'NZ-CI': {'name': 'Chatham Islands',
              'search': 'Chatham Islands, New Zealand'},
    'NZ-GI': {'name': 'Gisborne',
              'search': 'Gisborne, New Zealand'},
    'NZ-HB': {'name': 'Hawke\'s Bay',
              'search': 'Hawke\'s Bay, New Zealand'},
    'NZ-MW': {'name': 'Manawatu-Wanganui',
              'search': 'Manawatu-Wanganui, New Zealand'},
    'NZ-NE': {'name': 'Nelson',
              'search': 'Nelson, New Zealand'},
    'NZ-NO': {'name': 'Northland',
              'search': 'Northland, New Zealand'},
    'NZ-OT': {'name': 'Otago',
              'search': 'Otago, New Zealand'},
    'NZ-SO': {'name': 'Southland',
              'search': 'Southland, New Zealand'},
    'NZ-TK': {'name': 'Taranaki',
              'search': 'Taranaki, New Zealand'},
    'NZ-TS': {'name': 'Tasman',
              'search': 'Tasman, New Zealand'},
    'NZ-WK': {'name': 'Waikato',
              'search': 'Waikato, New Zealand'},
    'NZ-WG': {'name': 'Wellington',
              'search': 'Wellington, New Zealand'},
    'NZ-WC': {'name': 'West Coast',
              'search': 'West Coast, New Zealand'},
}

PH_REGIONS = {
    'PH-AB': {'name': 'Abra', 'search': 'Abra, Philippines'},
    'PH-AN': {'name': 'Agusan Del Norte', 'search': 'Agusan Del Norte, Philippines'},
    'PH-AS': {'name': 'Agusan del Sur', 'search': 'Agusan del Sur, Philippines'},
    'PH-AK': {'name': 'Aklan', 'search': 'Aklan, Philippines'},
    'PH-AL': {'name': 'Albay', 'search': 'Albay, Philippines'},
    'PH-AQ': {'name': 'Antique', 'search': 'Antique, Philippines'},
    'PH-AP': {'name': 'Apayao', 'search': 'Apayao, Philippines'},
    'PH-AU': {'name': 'Aurora', 'search': 'Aurora, Philippines'},
    'PH-BS': {'name': 'Basilan', 'search': 'Basilan, Philippines'},
    'PH-BA': {'name': 'Bataan', 'search': 'Bataan, Philippines'},
    'PH-BN': {'name': 'Batanes', 'search': 'Batanes, Philippines'},
    'PH-BT': {'name': 'Batangas', 'search': 'Batangas, Philippines'},
    'PH-BG': {'name': 'Benguet', 'search': 'Benguet, Philippines'},
    'PH-BI': {'name': 'Biliran', 'search': 'Biliran, Philippines'},
    'PH-BO': {'name': 'Bohol', 'search': 'Bohol, Philippines'},
    'PH-BK': {'name': 'Bukidnon', 'search': 'Bukidnon, Philippines'},
    'PH-BU': {'name': 'Bulacan', 'search': 'Bulacan, Philippines'},
    'PH-CG': {'name': 'Cagayan', 'search': 'Cagayan, Philippines'},
    'PH-CN': {'name': 'Camarines Norte', 'search': 'Camarines Norte, Philippines'},
    'PH-CS': {'name': 'Camarines Sur', 'search': 'Camarines Sur, Philippines'},
    'PH-CM': {'name': 'Camiguin', 'search': 'Camiguin, Philippines'},
    'PH-CP': {'name': 'Capiz', 'search': 'Capiz, Philippines'},
    'PH-CT': {'name': 'Catanduanes', 'search': 'Catanduanes, Philippines'},
    'PH-CV': {'name': 'Cavite', 'search': 'Cavite, Philippines'},
    'PH-CB': {'name': 'Cebu', 'search': 'Cebu, Philippines'},
    'PH-CL': {'name': 'Compostela Valley', 'search': 'Compostela Valley, Philippines'},
    'PH-NC': {'name': 'Cotabato', 'search': 'Cotabato, Philippines'},
    'PH-DV': {'name': 'Davao del Norte', 'search': 'Davao del Norte, Philippines'},
    'PH-DS': {'name': 'Davao del Sur', 'search': 'Davao del Sur, Philippines'},
    'PH-DO': {'name': 'Davao Oriental', 'search': 'Davao Oriental, Philippines'},
    'PH-DI': {'name': 'Dinagat Islands', 'search': 'Dinagat Islands, Philippines'},
    'PH-ES': {'name': 'Eastern Samar', 'search': 'Eastern Samar, Philippines'},
    'PH-GU': {'name': 'Guimaras', 'search': 'Guimaras, Philippines'},
    'PH-IF': {'name': 'Ifugao', 'search': 'Ifugao, Philippines'},
    'PH-IN': {'name': 'Ilocos Norte', 'search': 'Ilocos Norte, Philippines'},
    'PH-IS': {'name': 'Ilocos Sur', 'search': 'Ilocos Sur, Philippines'},
    'PH-II': {'name': 'Iloilo', 'search': 'Iloilo, Philippines'},
    'PH-IB': {'name': 'Isabela', 'search': 'Isabela, Philippines'},
    'PH-KA': {'name': 'Kalinga', 'search': 'Kalinga, Philippines'},
    'PH-LU': {'name': 'La Union', 'search': 'La Union, Philippines'},
    'PH-LG': {'name': 'Laguna', 'search': 'Laguna, Philippines'},
    'PH-LN': {'name': 'Lanao del Norte', 'search': 'Lanao del Norte, Philippines'},
    'PH-LS': {'name': 'Lanao del Sur', 'search': 'Lanao del Sur, Philippines'},
    'PH-LE': {'name': 'Leyte', 'search': 'Leyte, Philippines'},
    'PH-MG': {'name': 'Maguindanao', 'search': 'Maguindanao, Philippines'},
    'PH-MQ': {'name': 'Marinduque', 'search': 'Marinduque, Philippines'},
    'PH-MB': {'name': 'Masbate', 'search': 'Masbate, Philippines'},
    'PH-MM': {'name': 'Metropolitan Manila', 'search': 'Metropolitan Manila, Philippines'},
    'PH-MD': {'name': 'Misamis Occidental', 'search': 'Misamis Occidental, Philippines'},
    'PH-MN': {'name': 'Misamis Oriental', 'search': 'Misamis Oriental, Philippines'},
    'PH-MT': {'name': 'Mountain', 'search': 'Mountain, Philippines'},
    'PH-ND': {'name': 'Negros Occidental', 'search': 'Negros Occidental, Philippines'},
    'PH-NR': {'name': 'Negros Oriental', 'search': 'Negros Oriental, Philippines'},
    'PH-NS': {'name': 'Northern Samar', 'search': 'Northern Samar, Philippines'},
    'PH-NE': {'name': 'Nueva Ecija', 'search': 'Nueva Ecija, Philippines'},
    'PH-NV': {'name': 'Nueva Vizcaya', 'search': 'Nueva Vizcaya, Philippines'},
    'PH-MC': {'name': 'Occidental Mindoro', 'search': 'Occidental Mindoro, Philippines'},
    'PH-MR': {'name': 'Oriental Mindoro', 'search': 'Oriental Mindoro, Philippines'},
    'PH-PL': {'name': 'Palawan', 'search': 'Palawan, Philippines'},
    'PH-PM': {'name': 'Pampanga', 'search': 'Pampanga, Philippines'},
    'PH-PN': {'name': 'Pangasinan', 'search': 'Pangasinan, Philippines'},
    'PH-QZ': {'name': 'Quezon', 'search': 'Quezon, Philippines'},
    'PH-QR': {'name': 'Quirino', 'search': 'Quirino, Philippines'},
    'PH-RI': {'name': 'Rizal', 'search': 'Rizal, Philippines'},
    'PH-RO': {'name': 'Romblon', 'search': 'Romblon, Philippines'},
    'PH-SM': {'name': 'Samar', 'search': 'Samar, Philippines'},
    'PH-SG': {'name': 'Sarangani', 'search': 'Sarangani, Philippines'},
    'PH-SQ': {'name': 'Siquijor', 'search': 'Siquijor, Philippines'},
    'PH-SR': {'name': 'Sorsogon', 'search': 'Sorsogon, Philippines'},
    'PH-SC': {'name': 'South Cotabato', 'search': 'South Cotabato, Philippines'},
    'PH-SL': {'name': 'Southern Leyte', 'search': 'Southern Leyte, Philippines'},
    'PH-SK': {'name': 'Sultan Kudarat', 'search': 'Sultan Kudarat, Philippines'},
    'PH-SU': {'name': 'Sulu', 'search': 'Sulu, Philippines'},
    'PH-ST': {'name': 'Surigao del Norte', 'search': 'Surigao del Norte, Philippines'},
    'PH-SS': {'name': 'Surigao del Sur', 'search': 'Surigao del Sur, Philippines'},
    'PH-TR': {'name': 'Tarlac', 'search': 'Tarlac, Philippines'},
    'PH-TT': {'name': 'Tawi-Tawi', 'search': 'Tawi-Tawi, Philippines'},
    'PH-ZM': {'name': 'Zambales', 'search': 'Zambales, Philippines'},
    'PH-ZN': {'name': 'Zamboanga del Norte', 'search': 'Zamboanga del Norte, Philippines'},
    'PH-ZS': {'name': 'Zamboanga del Sur', 'search': 'Zamboanga del Sur, Philippines'},
    'PH-ZY': {'name': 'Zamboanga-Sibugay', 'search': 'Zamboanga-Sibugay, Philippines'},
}



# OTHER REGION/AREA GROUPINGS
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