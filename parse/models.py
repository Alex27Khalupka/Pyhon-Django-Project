from django.db import models


class Article(models.Model):
    title = models.CharField('article title', max_length = 200)
    description = models.TextField('description', max_length = 9000)
    image = models.CharField('image', max_length = 200)
    link = models.CharField('link', max_length = 200)
    date = models.CharField('date', max_length = 200)


    def __str__(self):
        return self.title


    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete = models.CASCADE)
    author_name = models.CharField('author name', max_length = 50)
    comment_text = models.CharField('comment text', max_length = 200)

    def __str__(self):
        return self.author_name

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


