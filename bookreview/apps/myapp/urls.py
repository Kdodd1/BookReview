from django.conf.urls import url 
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^create$', views.create),
	url(r'^login$',views.login),
	url(r'^logged$', views.logged),
	url(r'^review$', views.review),
	url(r'^userprofile/(?P<userid>\d+)$', views.userProfile),
	url(r'^bookprofile/(?P<bookid>\d+)$', views.bookProfile),
	url(r'^addreview$', views.addReview),
	url(r'^addreview2$', views.addReview2),
	url(r'^delete/(?P<reviewid>\d+)$', views.delete)
	]