from django.urls import path
from . import views

urlpatterns = [
	# ...existing code...
	path('scoringsheet/new/', views.scoringsheet_create, name='scoringsheet_create'),
	path('scoringsheet/success/', views.scoringsheet_success, name='scoringsheet_success'),
	path('embuscoringsheet/new/', views.embuscoringsheet_create, name='embuscoringsheet_create'),
	path('embuscoringsheet/success/', views.embuscoringsheet_success, name='embuscoringsheet_success'),
	# AJAX endpoint for testee search used by embuscoringsheet form
	path('ajax/testee-search/', views.ajax_testee_search, name='ajax_testee_search'),
	# ...existing code...
]