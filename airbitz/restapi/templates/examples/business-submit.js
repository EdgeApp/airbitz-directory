// create business object to post
var bizObj = {
  "provider_id": "airbitz-00001",
  "name": "Airbitz Wallet",
  "provider_url": "https://airbitz.co/biz/3384/airbitz-san-diego/",
  "description": "Airbitz provides the most fluid user experience in a Bitcoin wallet combined with a top quality, proximity searchable business directory of Bitcoin companies and merchants that accept Bitcoin.\
\
Airbitz believes strongly in company transparency and customer privacy. No information about wallet users' logins, passwords, bitcoin addresses, e-mails, or names are ever known by Airbitz or anyone other than the wallet users. All information is client side encrypted with industry standard AES256 using GPU resistant password derivation algorithms.",
  "website": "http://bizexample.com/",
  "phone": "610-323-1263",
  "street_address": "3919 30th street",
  "neighborhood": "North Park",
  "admin3_name": "San Diego", // city
  "admin2_name": "San Diego", // county
  "admin1_code": "CA", // US FIPS 5-2 1st level administrative division code (e.g., state/province)
  "postalcode": "92104",
  "country": "US", // ISO 3166-1 alpha-2 country code http://en.wikipedia.org/wiki/ISO_3166-1
  "physical_business": true,
  "online_business": true,
  "bitcoin_discount": 5,
  "score": 9,

  "location": {
    "latitude": 37.2350,
    "longitude": -115.8111
  },

  "categories": ["Food", "Restaurant"],

  "expense_category": "Expense:Food & Dining",

  "images": [
    {
      "url": "http://lorempixel.com/640/480/fashion/",
      "tags": ["primary"]
    },
    {
      "url": "http://lorempixel.com/640/480/nightlife/"
    },
    {
      "url": "http://lorempixel.com/640/480/people/"
    }
  ]
};

// set endpoint
var endpoint = '{{ ABSOLUTE_ROOT_URL }}api/v1/business/submit/';

// set token
$.ajax({
  beforeSend: function (xhr) {
    xhr.setRequestHeader (
      'Authorization',
      'Token YOUR_API_TOKEN'
    )
  },
  url: endpoint,
  type: 'POST',
  contentType:'application/json',
  data: JSON.stringify(bizObj),
  dataType:'json'
});