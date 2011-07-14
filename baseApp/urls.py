from django.conf.urls.defaults import *

urlpatterns = patterns('',
url(r'^$', 'baseApp.views.home'),
url(r'^bycategory$', 'baseApp.views.categories_list'),
#url(r'^byname$', 'baseApp.views.names_list'),
#url(r'^byvenue$', 'baseApp.views.venues_list'),
url(r'^events/(?P<id>\d+)$', 'baseApp.views.events_list'),
#url(r'^login$', 'reg.views.blog_list'),
url(r'^(detail|info)/(?P<id>\d+)$', 'baseApp.views.event_detail'),
url(r'^map/(?P<id>\d+)$', 'baseApp.views.view_map'),
<<<<<<< HEAD
url(r'^suggestions$', 'baseApp.views.addSuggestion'),
#url(r'^editsuggestion$', 'baseApp.views.editSuggestion'),
=======
url(r'^addEvent$', 'baseApp.views.addEvent_view'),
url(r'^suggestions$', 'baseApp.views.suggest_view'),
url(r'^tickets$', 'baseApp.views.ticket_view'),
#url(r'^eventPreview$', 'baseApp.views.ticket_view'),
#url(r'^signinInfo$', 'baseApp.views.addEvent_view'),
>>>>>>> e8a9c0b36769ffb42020e214b691aa856fe31138
#url(r'^search/(.+)*$', 'blog.views.blog_search'),
)
