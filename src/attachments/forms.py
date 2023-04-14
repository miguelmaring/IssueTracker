from django import forms 
from attachments.models import IssueAttachment
from django.forms import ClearableFileInput


class CustomClearableFileInput(ClearableFileInput):
    template_name = 'widgets/customclearablefileinput.html'
    

# Create your views here.
class NewIssueAttachmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = True

    class Meta:
        model = IssueAttachment
        fields = ['file']
        widgets = {
            'file': CustomClearableFileInput(attrs={'multiple': True}),
        }
        # widget is important to upload multiple files