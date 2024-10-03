# Импорт функции для отправки почты.
from django.core.mail import send_mail

# Пример вызова функции:
send_mail(
    subject='Тема письма',
    message='Текст сообщения',
    from_email='from@example.com',
    recipient_list=['to@example.com'],
    fail_silently=True,
)
