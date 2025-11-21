from django.db import models


class CallbackRequest(models.Model):
    name = models.CharField('Имя', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    service = models.ForeignKey('services.Service', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name='Услуга')
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    is_processed = models.BooleanField('Обработано', default=False)
    notes = models.TextField('Заметки', blank=True)

    class Meta:
        verbose_name = 'Заявка на обратный звонок'
        verbose_name_plural = 'Заявки на обратный звонок'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.phone}"