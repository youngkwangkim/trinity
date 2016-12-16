from django.conf.urls import include, url
from django.contrib import admin
from api_app.views import is_used
#from api_app.views import check

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^isUsed', is_used),
    #url(r'^api/check', check),
]
