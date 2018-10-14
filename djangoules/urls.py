from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required



urlpatterns = [
    # Examples:
    # url(r'^$', 'djangoules.views.home', name='home'),
    url(r'^web/', include('webapp.urls')),
    url(r'^', include('frontapp.urls')),
    url(r'^motor/', include('motorapp.urls')),
    #url(r'^cfg/', include('cfgapp.urls')),
    url(r'^restful/', include('mobapp.urls')),
    url(r'^promomanage/', include('dinamicasapp.urls')),
    #url(r'^admin/', include(admin.site.urls)),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)