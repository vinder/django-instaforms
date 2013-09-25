from django.conf.urls.defaults import url, patterns

from instaforms import views, forms


urlpatterns = patterns('',
    url(r'^sent/$', views.SentPage.as_view(), name="sent"),
    url(r'^(?P<formtype>[-\w]+)/$', views.InstaFormView.as_view(), name="instaform"),
    url(r'^jsrequired/$', views.JsRequiredPage.as_view(), name="jsrequired"),
)
