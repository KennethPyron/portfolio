from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Portfolio URLs
    path('portfolio/create/', views.portfolio_create, name='portfolio_create'),
    path('portfolio/<int:portfolio_id>/', views.portfolio_detail, name='portfolio_detail'),
    path('portfolio/<int:portfolio_id>/update/', views.portfolio_update, name='portfolio_update'),
    path('portfolio/<int:portfolio_id>/delete/', views.portfolio_delete, name='portfolio_delete'),

    # Project URLs
    path('projects/', views.project_list, name='project_list'),
    path('project/create/', views.project_create, name='project_create'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project/<int:project_id>/update/', views.project_update, name='project_update'),
    path('project/<int:project_id>/delete/', views.project_delete, name='project_delete'),

    # Student URLs
    path('students/', views.student_list, name='student_list'),
    path('student/create/', views.student_create, name='student_create'),
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),
    path('student/<int:student_id>/update/', views.student_update, name='student_update'),
    path('student/<int:student_id>/delete/', views.student_delete, name='student_delete'),

    # Authentication URLs (Django built-in)
    path('accounts/', include('django.contrib.auth.urls')),
]