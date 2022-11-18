from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify


class BasePost(models.Model):
    owner = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    text = models.TextField(max_length=2048, null=True)
    posted_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


    class Meta:
        abstract = True


class Board(BasePost):
    title = models.CharField(max_length=256, null=False)
    slug = models.SlugField(null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)


class Post(BasePost):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False)



class Comment(BasePost):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.text