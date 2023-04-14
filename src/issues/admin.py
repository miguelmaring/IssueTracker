from django.contrib import admin
from issues.models import Issue, Comment
from attachments.models import IssueAttachment

class IssueAttachmentInline(admin.TabularInline):
    model = IssueAttachment
    
class CommentsInline(admin.TabularInline):
    model = Comment


class IssueAdmin(admin.ModelAdmin):
    inlines = [
        IssueAttachmentInline,
        CommentsInline
    ]

# Register your models here.
admin.site.register(Issue, IssueAdmin)

