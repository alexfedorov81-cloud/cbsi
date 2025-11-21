from django.urls import path
from . import views

urlpatterns = [
    path('callback/', views.callback_request, name='callback'),
    # Убираем callback_success, так как он больше не нужен с AJAX
]