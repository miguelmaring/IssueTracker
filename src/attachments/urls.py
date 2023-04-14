from django.urls import path
from django.conf.urls.static import static 
from django.conf import settings

from attachments.views import (
    file_add_view,
    file_delete_view,
    file_download_view,
    file_open_view,
)

urlpatterns = [
    path('add/', file_add_view, name='add_file'),
    path('<int:file_id>/delete/', file_delete_view, name='delete_file'),
    path('<int:file_id>/download/', file_download_view, name='download_file'),
    path('<int:file_id>/open/', file_open_view, name='open_file'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)