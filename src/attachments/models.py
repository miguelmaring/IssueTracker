from django.db import models
from django.conf import settings
import os

# Create your models here.
class IssueAttachment(models.Model):
    file = models.FileField(upload_to="uploads")
    issue = models.ForeignKey("issues.Issue", on_delete=models.CASCADE)
        
    def filename(self):
        return os.path.basename(self.file.name)
    
    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.file.name))
        super(IssueAttachment,self).delete(*args,**kwargs)