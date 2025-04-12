from django.urls import path
from . import views

urlpatterns = [
    path('sidebar/', views.ai_sidebar, name='ai_sidebar'),
    path('query/', views.query_ai, name='query_ai'),
]
