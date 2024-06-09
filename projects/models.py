from django.db import models
import uuid

# Create your models here.


class Project(models.Model):
    title = models.CharField(max_length=200)
    video = models.CharField(max_length=200, null=True, blank=True, default='123')
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default='default.jpg')
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    networks = models.ManyToManyField('Network', blank=True)
    archive = models.BooleanField(null=True, blank=True, default=False)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    social_telegram = models.CharField(max_length=200, blank=True, null=True)
    social_x = models.CharField(max_length=200, blank=True, null=True)
    social_discord = models.CharField(max_length=200, blank=True, null=True)
    social_web = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = '/static/images/default.jpg'
        return url

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Network(models.Model):
    name = models.CharField(max_length=200)
    featured_image = models.ImageField(null=True, blank=True, default='default.jpg')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = '/static/images/default.jpg'
        return url

    @property
    def getProjectCount(self):
        """Возвращает количество проектов, связанных с этой сетью."""
        return self.project_set.count()


class Tool(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default='default.jpg')
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
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
