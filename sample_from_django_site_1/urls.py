from django.conf.urls import patterns, include, url
from polls import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sample_from_django_site_1.views.home', name='home'),
    # url(r'^sample_from_django_site_1/', include('sample_from_django_site_1.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
#    url(r'^$', views.index, name='index'),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
