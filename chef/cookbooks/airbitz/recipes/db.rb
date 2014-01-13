include_recipe 'postgresql::server'

$DB=node[:airbitz][:database][:name]
$DBUSER=node[:airbitz][:database][:username]
$DBPASS=node[:airbitz][:database][:password]

# Install postgis
package "postgresql-9.1-postgis" do
  action :install
end

# Install the auth file for postgres
template "#{node[:postgresql][:dir]}/pg_hba.conf" do
  cookbook 'airbitz'
end

# Only create the template and airbitz database once
bash "build_db" do
  user "postgres"
  creates "/var/lib/postgresql/.airbitz_installed"
  code <<-EOH
psql -c "DROP DATABASE IF EXISTS #{$DB};"
psql -c "DROP DATABASE IF EXISTS template_postgis;"
psql -c "DROP ROLE IF EXISTS #{$DBUSER};"

createdb --locale=en_US.utf8 -E UTF8 -T template0 template_postgis
psql -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql
psql -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql 
# psql -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-1.5/rtpostgis.sql
psql -d template_postgis -c "GRANT ALL ON geometry_columns TO PUBLIC;"
psql -d template_postgis -c "GRANT ALL ON geography_columns TO PUBLIC;"
psql -d template_postgis -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"

psql -c "create role #{$DBUSER} with login password '#{$DBUSER}'";
createdb --locale=en_US.utf8 -E UTF8 -T template_postgis #{$DB}
psql -d #{$DB} -c "grant all privileges on database #{$DB} to #{$DBUSER}";
touch /var/lib/postgresql/.airbitz_installed
  EOH
end
