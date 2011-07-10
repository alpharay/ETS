from django.conf.urls.defaults import *
urlpatterns = patterns('',
url(r'^$', 'blog.views.home'),url(r'^list/(\d+)?$', 'blog.views.blog_list'),
url(r'^(detail|info)/(?P<id>\d+)/((?P<showComments>.*)/)?$', 'blog.views.blog_detail'),
url(r'^search/(.+)*$', 'blog.views.blog_search'),
url(r'^editcomment/(?P<id>\d+)*/$', 'blog.views.edit_comment'),
url(r'^login/$', 'reg.views.loginView'),
url(r'^logout/$', 'reg.views.logoutView'),
url(r'^signup/$', 'reg.views.signupView'),
)
