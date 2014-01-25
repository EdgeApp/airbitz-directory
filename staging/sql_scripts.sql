
SELECT b.name, z.country, z.place_name, z.admin_name1, z.admin_name2
FROM directory_geonamezip z, directory_business b
WHERE b.center @ ST_Expand(z.center, 0.05)
  AND b.name ilike 'Spirito%'

-- Update postalcode, country and state for all places based of of lat/lon
UPDATE directory_business AS b
  set postalcode = z.postalcode,
      country = z.country,
      state = z.admin_code1
FROM location_geonamezip AS z
WHERE b.center @ ST_Expand(z.center, 0.05)
