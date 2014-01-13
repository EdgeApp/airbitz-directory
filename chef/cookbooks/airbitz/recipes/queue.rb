include_recipe 'airbitz'

# Install message queue
package "rabbitmq-server" do
  action :install
end

# Copy init scripts
cookbook_file "/etc/init.d/celeryd" do
  source "init/celeryd"
  mode 0766
end

# Copy defaults scripts
template "/etc/default/celeryd" do
  source "default/celeryd.erb"
  variables({
    :home => node[:airbitz][:app][:home],
    :user => node[:airbitz][:app][:user],
    :group => node[:airbitz][:app][:group],
  })
end

# Start workers
# service "celeryd" do
#   pattern "celeryd"
#   action [:enable, :start]
# end
