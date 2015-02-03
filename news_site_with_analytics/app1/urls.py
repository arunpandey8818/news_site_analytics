from django.conf.urls import patterns, url


urlpatterns = patterns('app1.views',
    url(r'^index/$', 'index'),
    url(r'^index/signup/$', 'signup'),
     
    url(r'^index/home/(?P<storyId>\d+)/$', 'detail'),

    url(r'^index/home/$', 'home'),
    url(r'^index/signup/home/$', 'home'),

    url(r'^index/user_prof/$', 'user_prof'),
    url(r'^index/user_profile/$', 'user_profile'),

    url(r'^index/my_view/$', 'my_view'),
    url(r'^index/signup/home/logout/$', 'logout_view'),
 
    url(r'^index/home/detail/$', 'detail'),
    url(r'^index/signup/home/detail/$', 'detail'),

    url(r'^index/home/analytics/$', 'analytics'),
    url(r'^index/signup/home/analytics/$', 'analytics'),

    url(r'^index/signup/home/analytics/tagusage/$', 'tagusage'),
    url(r'^index/home/analytics/tagusage/$', 'tagusage'),

    url(r'^index/signup/home/analytics/useractivity/$', 'useractivity'),
    url(r'^index/home/analytics/useractivity/$', 'useractivity'),
    
)
