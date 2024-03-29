from django.db import models


class Page(models.Model):
    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='pages')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='pages')
    followers = models.ManyToManyField('users.User', related_name='follows')
    image = models.CharField(max_length=200, null=True, blank=True)
    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField('users.User', related_name='requests')
    unblock_date = models.DateTimeField(null=True, blank=True)
    is_permanent_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    page = models.ForeignKey('Page', on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=180)
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.updated_at)


class Like(models.Model):
    post = models.ForeignKey('Post', on_delete=models.SET_NULL, related_name='likes', blank=True, null=True)
    owner = models.ForeignKey('users.User', on_delete=models.SET_NULL, related_name='likes', blank=True, null=True)

    def __str__(self):
        return str(self.owner)
