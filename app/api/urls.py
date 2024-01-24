from django.urls import path
from . import views


urlpatterns = [
	path('validate_bill/', views.ValidateBillView.as_view()),
]