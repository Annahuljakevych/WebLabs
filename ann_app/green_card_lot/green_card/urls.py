from django.urls import path
from . import views

app_name = 'green_card'
urlpatterns = [
	path('',views.index, name = 'index'),
	path('lottery',views.lottery, name = 'lottery'),
	path('register',views.register, name = 'register'),
	path('register/create',views.create, name = 'create'),
	path('log_in',views.log_in, name = 'log_in'),
	path('log_in/check',views.check, name = 'check'),
	path('log_out',views.log_out, name = 'log_out'),
	path('set_rus',views.set_rus, name = 'set_rus'),
	path('set_uzb',views.set_uzb, name = 'set_uzb'),
	path('set_tadz',views.set_tadz, name = 'set_tadz'),
	path('winner',views.get_winner, name = 'get_winner'),	
]