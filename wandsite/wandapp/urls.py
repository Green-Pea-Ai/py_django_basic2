from django.urls import path

from . import views

urlpatterns = [
	# ex: /wandapp/
	path('', views.index, name='index'),

	# ex: /wandapp/5/
	path('<int:question_id>/', views.detail, name='detail'),

	# ex: /wandapp/5/results/
	path('<int:question_id>/results/', views.results, name='results'),

	# ex: /wandapp/5/vote/
	path('<int:question_id>/vote/', views.vote, name='vote'),
]