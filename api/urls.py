from django.urls import path
from . import views

urlpatterns = [
    path('audio-verification/<str:name>/', views.audio_verification, name='audio-verification'),
    path('button-page/', views.button_page, name='button-page'),
    path('enroll-user/', views.enroll_user, name='enroll-user'),
    path('enroll-user-success/', views.enroll_user_success, name='enroll-user-success'),
    path('start-recording/', views.start_recording, name='start-recording'),
    path('success/', views.success_view, name='success_url'),
    path('failure/', views.failure_view, name='failure_url'),
]


