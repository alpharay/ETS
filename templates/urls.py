from django.conf.urls.defaults import *
urlpatterns = patterns('',
url(r'^$', 'reg.views.home'), 'reg.views.Welcome'),
url(r'^signup/$', 'blog.views.signup'),
url(r'^login/$', 'reg.views.loginView'),
url(r'^logout/$', 'reg.views.logoutView'),
)
