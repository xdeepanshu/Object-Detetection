from django.urls import path, include
from .views import list_view, upload, photo_detail


urlpatterns = [
    path('', list_view),
    path(r'list/', list_view, name='list'),
    path(r'upload/', upload, name='upload'),
    path(r'photo_detail/<public_id>', photo_detail, name='photo_detail'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/logout/', include('django.contrib.auth.urls'), name = 'logout'),
    ]
