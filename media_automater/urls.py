from django.conf.urls import *
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from media_automater import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'media_automater.views.home', name='home'),
    # url(r'^media_automater/', include('media_automater.foo.urls')),
    url(r'^home/$', 'media.views.home', name='home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Dajax
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),

    # Catch all for home
    url(r'^$', 'media.views.home', name='home'),
)

urlpatterns += staticfiles_urlpatterns()