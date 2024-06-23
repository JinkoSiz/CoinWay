import uuid
from django.db import models
from projects.models import Project


# Create your models here.

class Campaign(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default='default.jpg')
    projects = models.ManyToManyField(Project, blank=True, related_name='campaigns')
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = '/static/images/default.jpg'
        return url
