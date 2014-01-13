include_recipe 'airbitz'

$HOME=node[:airbitz][:app][:home]
$USER=node[:airbitz][:app][:user]
$GROUP=node[:airbitz][:app][:group]

package "nginx" do
  action :install
end

service "nginx" do
  supports :restart => true
  pattern "nginx"
  action [:enable, :start]
end

template "/etc/nginx/nginx.conf" do
  source "nginx-dev.conf.erb"
  mode 00644
  variables({
    :home => node[:airbitz][:app][:home],
  })
  notifies :restart, 'service[nginx]', :delayed
end

# airbitz
["media", "static"].each do |dir|
  directory "#{$HOME}/#{dir}" do
    owner $USER
    group $GROUP
    mode 00754
    action :create
  end
end
