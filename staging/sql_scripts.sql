SELECT b.name, z.country, z.place_name, z.admin_name1, z.admin_name2
FROM directory_geonamezip z, directory_business b
WHERE b.center @ ST_Expand(z.center, 0.05)
  AND b.name ilike 'Spirito%'

