from django.urls import path, include
from django.conf.urls.static import static 
from django.conf import settings

from issues.views import (
    issues_view,
    search_issue_view,
    issues_list_view,
    issues_filters_view,
    new_issue_view, 
    edit_issue_view, 
    delete_issue_view, 
    issue_details_view,
    issue_toggle_block_view,
    add_comment_view,
    assign_issue_me,
    bulk_new_issue_view,
)

urlpatterns = [
    path('', issues_view, name='home'),
    path('search_issue', search_issue_view, name='search_issue'),
    path('issues_list/<str:sort_by>/<str:order>/', issues_list_view, name='issues_list'),
    path('issues_filters/', issues_filters_view, name='issues_filters'),
    path('new/', new_issue_view, name='new_issue'),
    path('bulknew/', bulk_new_issue_view, name='bulk_new_issue'),
    path('<int:id>/', issue_details_view, name='issue_detail'),
    path('<int:id>/edit/', edit_issue_view, name='edit_issue'),
    path('<int:id>/delete/', delete_issue_view, name='delete_issue'),
    path('<int:id>/block/', issue_toggle_block_view, name='block_issue'),
    path('<int:id>/assign/me', assign_issue_me, name='assign_me'),
    path('<int:id>/comment/', add_comment_view, name='add_comment'),
    path('<int:id>/files/', include('attachments.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

