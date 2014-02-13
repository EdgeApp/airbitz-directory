
%w{static airbitz/static directory/static management/static}.each do |path| 
    guard 'less', :output => "airbitz/#{path}/css/" do
        watch(%r{^airbitz/#{path}/less/(.+\.less)$})
    end
end

# guard 'livereload' do
#     watch(%r{static/.+\.(css|js)})
#     watch(%r{templates/.+\.(html)})
#     watch(%r{airbitz/.+\.(py)})
# end

# vim:set ft=ruby sw=4 ts=4 et:
