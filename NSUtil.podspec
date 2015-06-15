
Pod::Spec.new do |s|
  s.name             = "NSUtil"
  s.version          = "0.1.3"
  s.summary          = "A short description of NSUtil."
  s.license          = 'MIT'
  s.author           = { "DevilMayCry4" => "237326369@163.com" }
  s.source           = { :git => "https://virgil_@bitbucket.org/virgil_/nsutil.git", :tag => s.version.to_s }
  s.platform     = :ios, '7.0'
  s.requires_arc = true
  s.homepage         = "https://github.com/artsy/Artsy-UIButtons"
  s.source_files = 'Pod/Classes/**/*'
  s.resource_bundles = {
    'NSUtil' => ['Pod/Assets/*.png']
  }
end
