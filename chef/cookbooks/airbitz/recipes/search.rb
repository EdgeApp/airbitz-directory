include_recipe 'airbitz'

# Install message queue
package "openjdk-6-jre" do
  action :install
end

template "/etc/profile.d/solr_env.sh" do
  source "solr/solr_env.sh.erb"
  mode 00755
  user "#{$USER}"
  group "#{$GROUP}"
  variables({
    :home => $HOME,
    :user => $USER
  })
end

template "/etc/init.d/solr" do
  source "solr/solr_init.sh.erb"
  mode 00755
  user "#{$USER}"
  group "#{$GROUP}"
  variables({
    :home => $HOME,
    :user => $USER
  })
end

template "#{$HOME}/solr_install.sh" do
  source "solr/solr_install.sh.erb"
  mode 00755
  user "#{$USER}"
  group "#{$GROUP}"
  variables({
    :home => $HOME
  })
end

script "install_something" do
  interpreter "bash"
  creates "#{$HOME}/solr"
  user "#{$USER}"
  cwd "#{$HOME}"
  code <<-EOH
  #{$HOME}/solr_install.sh
  EOH
end

template "#{$HOME}/solr/solr/collection1/conf/schema.xml" do
  source "solr/solr_schema.xml.erb"
  mode 00555
  user "#{$USER}"
  group "#{$GROUP}"
end

service "solr" do
  supports :restart => true
  pattern "solr"
  action [:enable, :start]
end

