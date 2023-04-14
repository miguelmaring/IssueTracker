from django.db import models
from datetime import datetime, date 
from django.conf import settings
from attachments.models import IssueAttachment

ISSUE_TYPE = [
    ('B', 'Bug'),
    ('Q', 'Question'),
    ('E', 'Enhancement'),
]

ISSUE_SEVERITY = [
    ('W', 'Whishlist'),
    ('M', 'Minor'),
    ('N', 'Normal'),
    ('I', 'Important'),
    ('C', 'Critical'),
]

ISSUE_PRIORITY = [
    ('L', 'Low'),
    ('N', 'Normal'),
    ('H', 'High'),
]


class Issue(models.Model):
    subject     = models.CharField(max_length=60)
    content     = models.TextField(max_length=280)
    type        = models.CharField(max_length=2, choices=ISSUE_TYPE, default='B')
    severity    = models.CharField(max_length=2, choices=ISSUE_SEVERITY, default='N')
    priority    = models.CharField(max_length=2, choices=ISSUE_PRIORITY, default='N')
    blocked     = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(blank=True, null=True)
    created_by  = models.ForeignKey("users.User", models.SET_NULL, blank=True, null=True, related_name="issue_creator")
    updated_by  = models.ForeignKey("users.User", models.SET_NULL, blank=True, null=True, related_name="issue_modifier")
    assigned_to = models.ForeignKey("users.User", models.SET_NULL, blank=True, null=True, related_name="assigned_user")
    deadline    = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    
    class Meta:
        verbose_name = ("Issue")
        verbose_name_plural = ("Issues")

    def __str__(self):
        return self.subject

class Comment(models.Model):
    issue       = models.ForeignKey(Issue, related_name="comments", on_delete=models.CASCADE)
    name        = models.CharField(max_length=80)
    content     = models.TextField(max_length=280)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return '%s - %s - %s - %s' % (self.issue.subject, self.content, self.name, self.created_at)

class Activity(models.Model):
    issue       = models.ForeignKey(Issue, related_name="activities", on_delete=models.CASCADE)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    formerSubject     = models.CharField(max_length=60, blank=True, null=True)
    formerContent     = models.TextField(max_length=280, blank=True, null=True)
    formerType        = models.CharField(max_length=2, choices=ISSUE_TYPE, blank=True, null=True)
    formerSeverity    = models.CharField(max_length=2, choices=ISSUE_SEVERITY, blank=True, null=True)
    formerPriority    = models.CharField(max_length=2, choices=ISSUE_PRIORITY, blank=True, null=True)

    latterSubject     = models.CharField(max_length=60, blank=True, null=True)
    latterContent     = models.TextField(max_length=280, blank=True, null=True)
    latterType        = models.CharField(max_length=2, choices=ISSUE_TYPE, blank=True, null=True)
    latterSeverity    = models.CharField(max_length=2, choices=ISSUE_SEVERITY, blank=True, null=True)
    latterPriority    = models.CharField(max_length=2, choices=ISSUE_PRIORITY, blank=True, null=True)

    attachments = models.ManyToManyField(IssueAttachment)

    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

