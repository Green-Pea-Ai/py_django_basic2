from django.urls import path

from . import views

app_name = 'wandapp'
urlpatterns = [
	# ex: /wandapp/
	path('', views.IndexView.as_view(), name='index'),

	# ex: /wandapp/5/
	# the 'name' value as called by the {% url %} template tag
	path('<int:pk>/', views.DetailView.as_view(), name='detail'),

	# ex: /wandapp/5/results/
	path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),

	# ex: /wandapp/5/vote/
	path('<int:question_id>/vote/', views.vote, name='vote'),
]