from django.conf.urls import patterns, include, url
from django.contrib import admin
from deals.categoryList import categoryList
from deals.itemList import itemList
from deals.getCrumb import getCrumb
from deals.account.view import register

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'learnProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^category/list/', categoryList),
    url(r'^item/', itemList),
    url(r'^v2/hong-kong/offer/list/',itemList),
    url(r'^crumb/get/',getCrumb),
    url(r'^register',register),
)
