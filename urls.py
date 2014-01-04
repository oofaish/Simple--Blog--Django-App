from django.conf.urls import patterns, url
from simple import views
from django.conf.urls import handler404, handler500

urlpatterns = patterns('',
    url( r'^int/$', views.staticViewJson, name="homePageView" ),
    url( r'^int/(?P<category>blog)/(?P<year>[\d]+)/(?P<slug>[\w\s-]+)/$', views.catPageViewJson, name="blogPostViewJason" ),
    url( r'^int/(?P<category>ideas)/(?P<year>[\d]+)/(?P<slug>[\w\s-]+)/$', views.catPageViewJson, name="ideaViewJason" ),
    url( r'^int/(?P<category>blog)/$', views.listViewJson, name="blogViewJason" ),
    url( r'^int/(?P<category>ideas)/$', views.listViewJson, name="ideasViewJason" ),
    url( r'^int/(?P<category>stuffilike)/$', views.stuffILikeViewJson, name="stuffILikeViewJson" ),
    url( r'^int/(?P<slug>[\w\s-]+)/$', views.staticViewJson, name="pageViewJason" ),

    #for all my various pages WITHOUT json
    url( r'^$', views.staticView, name="homePageView" ),
    url( r'^(?P<category>blog)/(?P<year>[\d]+)/(?P<slug>[\w\s-]+)/$', views.catPageView, name="blogPostView" ),
    url( r'^(?P<category>ideas)/(?P<year>[\d]+)/(?P<slug>[\w\s-]+)/$', views.catPageView, name="ideaView" ),
    url( r'^(?P<category>blog)/$', views.listView, name="blogView" ),
    url( r'^(?P<category>ideas)/$', views.listView, name="ideasView" ),
    url( r'^(?P<category>stuffilike)/$', views.stuffILikeView, name="stuffILikeView" ),
    url( r'^(?P<slug>[\w\s-]+)/$', views.staticView, name="pageView" ),
    
    url( r'^submitContactForm$', views.submitContactForm, name="submitContactForm" ),
    url( r'^submitKudos$', views.submitKudos, name="submitKudos" ),
)

