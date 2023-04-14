from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponseRedirect
from attachments.models import IssueAttachment
from attachments.forms import NewIssueAttachmentForm
from issues.models import Issue

def file_add_view(request, id):
    if request.method == 'POST':
        file_form = NewIssueAttachmentForm(request.POST, request.FILES)
        files = request.FILES.getlist('file') #field name in model
        if file_form.is_valid():
            issue_instance = Issue.objects.get(pk = id)
            for f in files:
                attachment_instance = IssueAttachment(file=f, issue=issue_instance)
                attachment_instance.save()
            return redirect('issue_detail', id)
        
# View to download files
def file_download_view(request, id, file_id):
    file = IssueAttachment.objects.get(pk=file_id)
    return FileResponse(file.file, as_attachment=True)

def file_open_view(request, id, file_id):
    file = IssueAttachment.objects.get(pk=file_id)
    return FileResponse(file.file)

def file_delete_view(request, id, file_id):
    file = IssueAttachment.objects.get(pk=file_id)
    file.delete()
    return redirect('issue_detail', id)
    