include_recipe 'build-essential'

$USER=node[:airbitz][:app][:user]
$GROUP=node[:airbitz][:app][:group]
$HOME=node[:airbitz][:app][:home]
$BASE="#{$HOME}/airbitz"
$VENV="#{$BASE}/ENV"

# Setup the user and group
group $GROUP do end

user $USER do
  gid $USER
  home "/home/#{$USER}"
  shell "/bin/bash"
  supports :manage_home => true
end

# Install packages
%w{python-dev python-virtualenv libncurses5-dev 
   libgeos-dev libgeos-3.2.2 libgdal1-1.7.0 
   vim git libtiff4-dev libjpeg8-dev zlib1g-dev 
   libfreetype6-dev liblcms1-dev libwebp-dev unzip
   geoip-bin geoip-database geoip-database-contrib}.each do |pkg|
  package pkg do
    action :install
  end
end

%w{libjpeg.so libfreetype.so libz.so}.each do |lib|
  link "/usr/lib/#{lib}" do
    to "/usr/lib/x86_64-linux-gnu/#{lib}"
  end
end

# airbitz
directory "#{$BASE}" do
  owner $USER
  group $GROUP
  mode 00754
  action :create
end

# setup locale stuff
cookbook_file "/etc/default/locale" do
  source "locale"
  mode 00644
end

bash "update_locale" do
  code <<-EOH
locale-gen en_US.UTF-8
dpkg-reconfigure locales
  EOH
end

execute "geoip-database-contrib_update" do
  command "geoip-database-contrib_update"
  user "root"
end

# Create our environment
execute "virtualenv" do
  command "virtualenv ENV"
  user $USER
  group $GROUP
  cwd $BASE
end

# Copy install_db.sh 
template "#{$HOME}/install_db.sh" do
  source "install_db.sh.erb"
  mode 00754
  owner $USER
  group $GROUP
  variables({
    :db => node[:airbitz][:database][:name],
    :user => node[:airbitz][:database][:username]
  })
end

# Copy shell scripts
%w{quick_bitz.sh}.each do |file|
  cookbook_file "#{$HOME}/#{file}" do
    source file
    mode 00754
    owner $USER
    group $GROUP
  end
end

# Copy pgpass 
template "#{$HOME}/.pgpass" do
  source "pgpass.erb"
  mode 0600
  owner $USER
  group $GROUP
  variables({
    :db => node[:airbitz][:database][:name],
    :username => node[:airbitz][:database][:username],
    :password => node[:airbitz][:database][:password],
  })
end

# Link airbitz into virtualenv
link "#{$VENV}/airbitz" do
    to "/airbitz"
    owner $USER
    group $GROUP
end

bash "update_pip" do
  user $USER
  cwd $VENV
  code <<-EOH
source ./bin/activate
export PIP_DEFAULT_TIMEOUT=800
pip install -r /staging/requirements.txt --default-timeout=800 --timeout=800 --quiet
  EOH
# pip install -r /staging/requirements.txt --use-mirrors --default-timeout=800 --timeout=800 --quiet
end
