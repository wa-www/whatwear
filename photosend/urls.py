from django.contrib import admin
from django.urls import path
from . import views



app_name='photosend'
urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('new', views.photos_new, name='new'),
    path('mosaic', views.edit_mosaic, name='mosaic'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:comment_pk>/comment_delete/', views.comment_delete, name='comment_delete'),
    path('<int:pk>/', views.photo_detail, name='photo_detail'),
    path('edit/<int:pk>', views.photo_edit, name='edit'),
    path('<int:user_pk>/index/', views.user_index, name='user_index'),
    path('like/', views.like, name='like'),
]
