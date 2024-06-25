from django.urls import path
from . import views


urlpatterns = [
    path('', views.projects, name='projects'),
    path('tools/', views.tools, name='tools'),
    path('tool/<str:pk>/', views.tool, name='tool'),
    path('project/<str:pk>/', views.project, name='project'),
    path('news/', views.news, name='news'),
    path('load_more_projects/', views.load_more_projects, name='load_more_projects'),
]
