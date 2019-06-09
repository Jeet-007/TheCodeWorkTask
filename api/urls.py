from django.conf.urls import url
from api.views import TodoView, TodoExtraView

app_name = 'api'

urlpatterns = [
	url(r'^todo/$', TodoView.as_view(), name='todoview'),
	url(r'^todo_complete/$', TodoExtraView.as_view(), name='todoextraview'),
	]