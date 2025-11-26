from django.db import models


class Service(models.Model):
    IMAGE_CHOICES = [
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
        ('car', 'Автомобиль - выезд'),
        ('heart', 'Сердце - отношения'),
        ('chart-line', 'График - мониторинг'),
        ('exclamation-triangle', 'Треугольник - профилактика'),
    ]

    title = models.CharField('Название услуги', max_length=200)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    duration = models.CharField('Продолжительность', max_length=50)
    is_active = models.BooleanField('Активна', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    # Обновленное поле для картинки с новыми иконками
    image = models.CharField(
        'Иконка',
        max_length=50,
        choices=IMAGE_CHOICES,
        default='user-shield',
        help_text='Выберите иконку для услуги'
    )

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['order']

    def __str__(self):
        return self.title