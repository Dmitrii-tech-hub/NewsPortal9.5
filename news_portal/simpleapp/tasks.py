from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.timezone import now
from .models import Post, Category

def send_weekly_newsletter():
    # Получаем текущую дату и дату за неделю до неё
    today = now()
    last_week = today - timedelta(days=7)

    # Получаем все посты, созданные за последнюю неделю
    posts = Post.objects.filter(created_at__gte=last_week)

    if not posts.exists():
        return

    # Проходим по всем категориям
    for category in Category.objects.all():
        # Для каждой категории получаем подписчиков
        subscribers = category.subscribers.all()

        # Если подписчики есть и посты по категории найдены
        category_posts = posts.filter(categories=category)
        if category_posts.exists() and subscribers.exists():
            # Генерируем HTML-содержание письма
            html_content = render_to_string(
                'weekly_posts_email.html',  # Шаблон письма
                {
                    'posts': category_posts,
                    'category': category,
                }
            )

            # Отправляем письмо каждому подписчику
            for subscriber in subscribers:
                subject = f"Еженедельная рассылка новостей в категории {category.name}"
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=f"Новые статьи за неделю в категории {category.name}.",
                    from_email='your-email@example.com',
                    to=[subscriber.email]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()

    print("Weekly newsletter sent.")
