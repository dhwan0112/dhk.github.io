source "https://rubygems.org"

gem "jekyll", "~> 4.3"
gem "webrick"

# Pin sass-embedded below the broken 1.100.0 release.
# sass-embedded 1.100.0 (released 2026-05-22) fails to build its native
# extension with "uninitialized constant JSON::Fragment" in
# ext/sass/sass_config.rb, breaking every CI build that resolves it via
# jekyll -> jekyll-sass-converter -> sass-embedded. Remove this pin once
# upstream ships a fixed release.
gem "sass-embedded", "< 1.100"

group :jekyll_plugins do
  gem "jekyll-feed"
  gem "jekyll-seo-tag"
  gem "jekyll-sitemap"
end
