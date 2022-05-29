from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Название', max_length=50)
    content = models.TextField('Описание', blank=True)
    pub_date_post = models.DateTimeField('Дата публикации', auto_now_add=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/')
    likes = models.ManyToManyField(User, related_name='blog_posts')
    views = models.ManyToManyField(User, related_name='view_posts')
    tags = models.ManyToManyField('Tag', blank=True, related_name='tag_posts')

    def __str__(self):
        return f"{self.title}"

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def total_likes(self):
        return self.likes.count()

    def total_views(self):
        return self.views.count()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-pub_date_post']


class Tag(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    author_name = models.CharField("Автор", max_length=50)
    comment_text = models.CharField("Комментарий", max_length=200)
    pub_date_comment = models.DateTimeField("Дата публикации", auto_now_add=True)

    def __str__(self):
        return f"{self.author_name}"

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date_comment']
