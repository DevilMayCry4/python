from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from deals.categoryList import categoryList
from deals.itemList import itemList
from deals.getCrumb import getCrumb
from deals.account.view import register
from deals.views import login
from django.conf.urls.static import static
import learnProject.settings


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'learnProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^v0/hong-kong/category/list/', categoryList),
    url(r'^item/', itemList),
    url(r'^v2/hong-kong/offer/list/',itemList),
    url(r'^crumb/get/',getCrumb),
    url(r'^v0/hong-kong/register',register),
    url(r'^v0/hong-kong/login',login),
)

urlpatterns += static(settings.STATIC_URL)
#urlpatterns += static(learnProject.settings.MEDIA_URL , document_root = learnProject.settings.MEDIA_ROOT )
#urlpatterns += static(learnProject.settings.STATIC_URL, document_root = learnProject.settings.STATIC_ROOT )