from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^advertise/$', TemplateView.as_view(template_name='advertise.html'),
        name='advertise'),
    url(r'^shopify/$', TemplateView.as_view(template_name='shopify.html'),
        name='shopify'),
    url(r'^video/$', TemplateView.as_view(template_name='video.html'),
        name='video'),
    # url(r'^hackathon/', include('hackathon.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)