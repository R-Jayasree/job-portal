from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.firstpage, name='welcome'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('home/',TemplateView.as_view(template_name='home.html'), name='home'),
    path('createjs/', views.create_job_seeker, name='createjs'),
    path('createjr/', views.create_job_recruiter,  name='createjr'),

    path('home/profile/', views.profile_view,  name='profile'),
    path('home/update',views.update_profile,name='update_profile'),

    path('home/updatejs/', views.update_profile_seeker, name='updatejs'),
    path('home/updatejr/', views.update_profile_recruiter, name='updatejr'),
    path('home/delete',views.delete_profile,name='delete_profile'),

    path('home/recommendations/jobs/', views.job_list, name='job_list'),
    path('home/recommendations/details', views.view_details, name='details'),
    path('home/recommendations/remove',views.remove_from_recommendations, name='remove'),
    path('home/recommendations/seekers/', views.seekers_list, name='seekers_list'),
    path('home/recommendations/', views.recommendations, name='recommendations'),

    path('home/search/', views.search_view, name='search'),
    path('home/search/seekers/', views.search_seekers, name='search_seekers'),
    path('home/search/jobs/', views.search_jobs, name='search_jobs'),

    path('home/recommendations/apply', views.apply_job, name='apply_job'),
    path('home/recommendations/select', views.select_seeker, name='select_seeker'),
    path('home/notifications/', views.notification_view , name='notifications'),

    path('home/recommendations/details/faq', views.faq_view, name = 'faq'),
]