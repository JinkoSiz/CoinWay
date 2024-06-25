from django.urls import path
from . import views


urlpatterns = [
    path('', views.projects, name='projects'),
    path('tools/', views.tools, name='tools'),
    path('tool/<str:pk>/', views.tool, name='tool'),
    path('project/<str:pk>/', views.project, name='project'),
    path('news/', views.news, name='news'),

    path('api/projects/', views.api_projects, name='api_projects'),
]
