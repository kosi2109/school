from django.urls import path
from .views import *
app_name = 'rollcall'

urlpatterns = [
	path('',home , name="home"),
	path('login/',userLogin , name="login"),
	path('logout/',userLogout , name="logout"),

	path('join/',join , name="join"),
	path('joined/',joined , name="joined"),
	path('post/',post , name="post"),
	path('door/',door , name="door"),
	path('classDetail/<str:name>/',classDetail , name='classDetail'),
	path('getStudents/<str:room>/',getStudents , name='getStudents'),
]