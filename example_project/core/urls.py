from django.conf.urls import include, url
import migdal.urls

from django.contrib import admin


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
] + migdal.urls.urlpatterns
