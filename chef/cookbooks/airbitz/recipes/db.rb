$DB=node[:airbitz][:database][:name]
$DBUSER=node[:airbitz][:database][:username]
$DBPASS=node[:airbitz][:database][:password]

bash "add_repository" do
  code <<-EOH
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" >> /etc/apt/sources.list.d/postgresql.list
apt-get update
  EOH
  creates "/etc/apt/sources.list.d/postgresql.list"
end

# Install postgis
%w{libpq-dev postgresql-9.3-postgis-2.1 postgresql-9.3-postgis-scripts postgresql-contrib-9.3}.each do |pkg|
  package pkg do
    action :install
  end
end

# Install the auth file for postgres
# template "#{node[:postgresql][:dir]}/pg_hba.conf" do
#   cookbook 'airbitz'
# end

# Only create the template and airbitz database once
bash "build_db" do
  user "postgres"
  creates "/var/lib/postgresql/.airbitz_installed"
  code <<-EOH
psql -c "DROP DATABASE IF EXISTS #{$DB};"
psql -c "DROP DATABASE IF EXISTS template_postgis2;"
psql -c "DROP ROLE IF EXISTS #{$DBUSER};"

createdb -E UTF8 template_postgis2.1
psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='template_postgis2.1'"
psql -d template_postgis2.1 -f /usr/share/postgresql/9.3/extension/postgis--2.1.7.sql
psql -d template_postgis2.1 -c "GRANT ALL ON geometry_columns TO PUBLIC;"
psql -d template_postgis2.1 -c "GRANT ALL ON geography_columns TO PUBLIC;"
psql -d template_postgis2.1 -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"

psql -c "create role #{$DBUSER} with login password '#{$DBUSER}'";
createdb -T template_postgis2.1 #{$DB}
psql -d #{$DB} -c "grant all privileges on database #{$DB} to #{$DBUSER}";
touch /var/lib/postgresql/.airbitz_installed
  EOH
end
