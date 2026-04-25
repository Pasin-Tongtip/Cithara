from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('library/', views.library_view, name='library'),
    path('logout/', views.custom_logout, name='logout'),

    path('create/', views.create_song, name='create_song'),
    path('song/<int:song_id>/review/', views.review_song, name='review_song'),
    path('song/<int:song_id>/share/', views.share_song, name='share_song'),
    path('song/<int:song_id>/status/', views.check_song_status, name='check_song_status'),
    path('song/<int:song_id>/edit/', views.edit_song, name='edit_song'),
    path('song/<int:song_id>/delete/', views.delete_song, name='delete_song'),

    path('song/<int:song_id>/download/<str:format>/', views.download_song, name='download_song'),

    path('song/<int:song_id>/api/generate/', views.generate_song_api, name='generate_song_api'),
    path('song/<int:song_id>/api/status/', views.check_suno_status, name='check_suno_status'),
]
