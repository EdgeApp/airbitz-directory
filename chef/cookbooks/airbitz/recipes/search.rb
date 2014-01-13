include_recipe 'airbitz'

# Install message queue
package "openjdk-6-jre" do
  action :install
end
