from django.db import models


class Post(models.Model):
    picture = models.ImageField(upload_to='image')
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=5096)
    create_data = models.DateTimeField(auto_created=True)
    comments = models.ManyToManyField('Comment', blank=True)


class Comment(models.Model):
    comment = models.ManyToManyField('self', blank=True)
    text = models.CharField(max_length=1024)
