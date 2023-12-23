from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('features', views.features, name='features'),
    path('user_dashboard', views.user_dashboard, name='user_dashboard'),
    path('about', views.about, name='about'),
    path('express_interest', views.express_interest, name='express_interest'),
    path('packages/', views.package_list, name='package_list'),
    path('send_notification/', views.send_interest_notification, name='send_interest_notification'),
    path('enroll/<int:package_id>/', views.enroll_package, name='enroll_package'),
   path('generate-result/', views.generate_result, name='generate_result'),
]
