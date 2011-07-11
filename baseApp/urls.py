from django.conf.urls.defaults import *

urlpatterns = patterns('',
url(r'^$', 'baseApp.views.home'),
url(r'^bycategory$', 'baseApp.views.categories_list'),
#url(r'^byname$', 'baseApp.views.names_list'),
#url(r'^byvenue$', 'baseApp.views.venues_list'),
url(r'^events/(?P<id>\d+)$', 'baseApp.views.events_list'),
#url(r'^login$', 'reg.views.blog_list'),
url(r'^(detail|info)/(?P<id>\d+)$', 'baseApp.views.event_detail'),
#url(r'^search/(.+)*$', 'blog.views.blog_search'),
#url(r'^editcomment/(?P<id>\d+)*/$', 'blog.views.edit_comment'),
)
