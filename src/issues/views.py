from copy import deepcopy
import datetime
import mimetypes
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from issues.models import Issue, Comment, Activity
from issues.forms import NewIssueForm, CommentForm, DateInput, BulkNewIssueForm
from attachments.models import IssueAttachment
from attachments.forms import NewIssueAttachmentForm
from users.models import Log


def principal(request):
    return render(request, 'home.html')

def search_issue_view(request):  
    if request.method == "POST":
        searched = request.POST['searched']
        issues = Issue.objects.filter(subject__contains = searched) | Issue.objects.filter(content__contains = searched)
        return render(request, 'search_issue.html', {'searched' : searched, 'issues' : issues})
    else:
        return render(request, 'search_issue.html', {})


def issues_view(request):
    context = {}
    context['issues'] = Issue.objects.order_by('-id')  
    return render(request, 'issues.html', context)

def issues_list_view(request, sort_by, order):
    if order == 'desc':
        sort_by = f'-{sort_by}'
    issues = Issue.objects.all().order_by(sort_by)
    context = {'issues': issues}
    return render(request, 'issues.html', context)

def issues_filters_view(request):
    type_filter = request.GET.get("type", "")
    severity_filter = request.GET.get("severity", "")
    priority_filter = request.GET.get("priority", "")

    issues = Issue.objects.all()

    if type_filter:
        issues = issues.filter(type=type_filter)
    if severity_filter:
        issues = issues.filter(severity = severity_filter)
    if priority_filter:
        issues = issues.filter(priority = priority_filter)
    context = {"issues" : issues}
    return render(request, "issues.html",context)

# View to create a new issue
def new_issue_view(request):
    context = {}
    context['title_value'] = "New Issue"
    if request.method == 'POST':
        form = NewIssueForm(request.POST)
        if form.is_valid():
            issue_instance = form.save(commit=False)
            if request.user.is_authenticated:
                issue_instance.created_by = request.user
                
            issue_instance.save()
            
            # We create the log and link it to the user.
            new_log = Log.objects.create(issue=issue_instance, change_type='create', issue_name=issue_instance.subject, issue_deadline=issue_instance.deadline) 
            request.user.logs.add(new_log)
            
            return redirect('issue_detail', issue_instance.pk)
    else:
        form = NewIssueForm()
        context['issues_form'] = form
    return render(request, 'new_issue.html', context)

# View to create a bunch of new issues
def bulk_new_issue_view(request):
    context = {}
    context['title_value'] = "New Issue"
    if request.method == 'POST':
        print(request.POST)  # Add this line to check if the POST data is being correctly passed
        form = BulkNewIssueForm(request.POST)
        if form.is_valid():
            titles = form.cleaned_data['titles']
            title_list = titles.split('\n')
            for title in title_list:
                issue_instance = Issue.objects.create(subject=title.strip())

                # We create the log and link it to the user.
                new_log = Log.objects.create(issue=issue_instance, change_type='create', issue_name=issue_instance.subject) 
                request.user.logs.add(new_log)

            return redirect('home')
        else:
            print(form.errors)  # Add this line to check if there are any form errors
    else:
        form = BulkNewIssueForm()
        context['issues_form'] = form

    return render(request, 'bulk_new_issue.html', context)

# View to edit an issue
def edit_issue_view(request, id):
    issue = Issue.objects.get(pk=id)
    context = {'edit': issue}
    context['title_value'] = "Edit Issue"
    
    issue_cp = deepcopy(issue)
    if request.method == 'POST':
        form = NewIssueForm(request.POST or None, instance=issue)
        if form.is_valid():
            edited_issue = form.save(commit=False)
            if request.user.is_authenticated:
                edited_issue.updated_at = datetime.datetime.now()
                edited_issue.updated_by = request.user
            edited_issue.save()
            
            new_act = Activity.objects.create(issue=issue, user=request.user)
            
            messages.success(request, 'Issue actualizado con éxito')
            # We create the log and link it to the user.
            
            something = False

            if form.cleaned_data['subject'] != issue_cp.subject:
                new_act.formerSubject = issue_cp.subject
                new_act.latterSubject = form.cleaned_data['subject']
                something = True
            if form.cleaned_data['content'] != issue_cp.content:
                new_act.formerContent = issue_cp.content
                new_act.latterContent = form.cleaned_data['content']
                something = True
            if form.cleaned_data['type'] != issue_cp.type:
                new_act.formerType = issue_cp.type
                new_act.latterType = form.cleaned_data['type']
                something = True
            if form.cleaned_data['severity'] != issue_cp.severity:
                new_act.formerSeverity = issue_cp.severity
                new_act.latterSeverity = form.cleaned_data['severity']
                something = True
            if form.cleaned_data['priority'] != issue_cp.priority:
                new_act.formerPriority = issue_cp.priority
                new_act.latterPriority = form.cleaned_data['priority']
                something = True
            if new_act.attachments.exists():
                something = True

            # If there is nothing new, don't create the Activity    
            if something:
                new_act.save()
            else:
                new_act.delete()

            
            
            new_log = Log.objects.create(issue=edited_issue, change_type='edit', issue_name=edited_issue.subject) 
            request.user.logs.add(new_log)
            return redirect('issue_detail', id)
        
        else:
            for error in form.errors:
                print(error)
            context['issues_form'] = form
    else:
        form = NewIssueForm(instance=issue)
        context['issues_form'] = form
    return render(request, 'new_issue.html', context)

# View to delete an issue
def delete_issue_view(request, id):
    issue = Issue.objects.get(pk=id)

    # We create the log and link it to the user.
    new_log = Log.objects.create(issue=None, change_type='delete', issue_name=issue.subject) 
    request.user.logs.add(new_log)

    issue.delete()
    messages.success(request, 'Issue borrado con éxito')

    return redirect('home')

# View to see the details of an issue
def issue_details_view(request, id):
    issue = Issue.objects.get(pk=id)
    files = IssueAttachment.objects.filter(issue__pk=id)
    comments = Comment.objects.filter(issue=issue).order_by('-created_at') 
    activities = Activity.objects.filter(issue=issue).order_by('-created_at')    
    comment_form = CommentForm()
    file_form = NewIssueAttachmentForm()
    context = {'issue': issue, 'comments': comments, 'comment_form': comment_form, 'files': files, 'file_form': file_form, 'activities': activities}
    return render(request, 'show_issue.html', context)

def issue_toggle_block_view(request, id):
    issue = Issue.objects.get(pk=id)
    if issue.blocked:
        issue.blocked = False
    else:
        issue.blocked = True
    issue.save()
    #issue.blocked = not issue.blocked
    return redirect('issue_detail', id)

def assign_issue_me (request, id):
    issue = Issue.objects.get(pk=id)
    issue.assigned_to = request.user
    issue.save()
    return redirect('issue_detail', id)

def add_comment_view(request, id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            name = request.user.username
            issue = issue = Issue.objects.get(pk=id)
            newComment = form.save(commit=False)
            newComment.issue = issue
            newComment.name = name
            newComment.save()
    return redirect('issue_detail', id)

# View to add watcher
def add_watcher(request, id):
    issue = Issue.objects.get(pk=id)
    request.user.issues_watched.add(issue)    
    return redirect('issue_detail', id)

# View to delete watcher
def delete_watcher(request, id):
    issue = Issue.objects.get(pk=id)
    request.user.issues_watched.remove(issue)
    return redirect('issue_detail', id)