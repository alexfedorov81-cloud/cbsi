from django.db import models


class Service(models.Model):
    title = models.CharField('Название услуги', max_length=200)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    duration = models.CharField('Продолжительность', max_length=50)
    is_active = models.BooleanField('Активна', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    # Новое поле для картинки
    image = models.CharField('Иконка', max_length=50, blank=True,
                             choices=[
                                 ('user-shield', 'Защита пользователя'),
                                 ('briefcase', 'Портфель - бизнес'),
                                 ('users', 'Группа людей'),
                                 ('search', 'Поиск - расследования'),
                                 ('shield-alt', 'Щит - безопасность'),
                                 ('eye', 'Глаз - наблюдение'),
                                 ('file-contract', 'Документ - проверка'),
                                 ('balance-scale', 'Весы - справедливость'),
                                 ('id-card', 'ID карта - персонал'),
                                 ('lock', 'Замок - конфиденциальность'),
                             ],
                             default='user-shield',
                             help_text='Выберите иконку для услуги')
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['order']

    def __str__(self):
        return self.title