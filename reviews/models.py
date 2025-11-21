from django.db import models

from django.db import models


class Review(models.Model):
    RATING_CHOICES = [
        (5, '★★★★★'),
        (4, '★★★★'),
        (3, '★★★'),
        (2, '★★'),
        (1, '★'),
    ]

    author_name = models.CharField('Имя автора', max_length=100)
    text = models.TextField('Текст отзыва')
    rating = models.PositiveSmallIntegerField('Рейтинг', choices=RATING_CHOICES)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    is_published = models.BooleanField('Опубликовано', default=False)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author_name} - {self.rating}★"