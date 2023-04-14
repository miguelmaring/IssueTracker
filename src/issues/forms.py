from django import forms 
from django.db import models

from issues.models import (
    Issue, 
    ISSUE_PRIORITY, 
    ISSUE_SEVERITY, 
    ISSUE_TYPE,
    Comment
)
class DateInput(forms.DateInput):
    
    input_type= 'date'

class NewIssueForm(forms.ModelForm):
    subject     = forms.CharField(max_length=80, required=True)
    content     = forms.CharField(max_length=280 ,widget=forms.Textarea, required=True)
    type        = forms.ChoiceField(choices=ISSUE_TYPE)
    severity    = forms.ChoiceField(choices=ISSUE_SEVERITY)
    priority    = forms.ChoiceField(choices=ISSUE_PRIORITY)
    deadline    = forms.DateField(widget=DateInput, required=False)

    class Meta:
        model = Issue
        fields = '__all__'
        exclude = ['blocked', 'created_at', 'created_by', 'updated_at', 'updated_by', 'assigned_to']

        widgets={
            'subject' : forms.TextInput(attrs={'class':'form-control'}),
            'content' : forms.TextInput(attrs={'class':'form-control'}),
            'type' : forms.ChoiceField(choices=ISSUE_TYPE),
            'severity' : forms.ChoiceField(choices=ISSUE_SEVERITY),
            'priority' : forms.ChoiceField(choices=ISSUE_PRIORITY),
            'deadline' : DateInput(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        
class BulkNewIssueForm(forms.Form):
    titles = forms.CharField(widget=forms.Textarea)
