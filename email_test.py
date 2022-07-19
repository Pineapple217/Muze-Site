from django.core.mail import send_mail

send_mail(
    'Django Testmail',
    'Here is the message.',
    'muze@achim.be',
    ['rosierjules@gmail.com'],
    fail_silently=False,
)