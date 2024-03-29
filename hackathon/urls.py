from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from hackathon import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^advertise/$', views.AdvertiseView.as_view(), name='advertise'),
    url(r'^advertise/demo/$', views.advertise_demo, name='advertise_demo'),
    url(r'^advertise/demo_success/$', views.advertise_demo_success, name='advertise_demo_success'),
    url(r'^shopify/$', TemplateView.as_view(template_name='shopify.html'),
        name='shopify'),
    url(r'^video/$', TemplateView.as_view(template_name='video.html'),
        name='video'),

    url(r'^shopify/connect/$', views.shopify_connect, name='shopify_connect'),
    url(r'^shopify/connected/$', views.shopify_connected,
        name='shopify_connected'),
    url(r'^shopify/demo/$', views.shopify_demo, name='shopify_demo'),

    url(r'^facebook/pages.json$', views.facebook_pages, name='facebook_pages'),
    url(r'^facebook/advertise/$', views.facebook_advertise,
        name='facebook_advertise'),
    url(r'^facebook/snippets/$', views.facebook_snippets,
        name='facebook_snippets'),

    url(r'^thanks/$', TemplateView.as_view(template_name='thanks.html'),
        name='thanks'),

    # url(r'^hackathon/', include('hackathon.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
