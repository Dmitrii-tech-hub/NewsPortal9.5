from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        html_content = render_to_string(
            'welcome_email.html',
            {
                'user': instance,
            }
        )
        msg = EmailMultiAlternatives(
            subject='Добро пожаловать!',
            body='Добро пожаловать в наш новостной портал!',
            from_email='dmitrij.croitoru@yandex.com',
            to=[instance.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
