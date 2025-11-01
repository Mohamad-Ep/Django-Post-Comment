from celery import shared_task
from .models import Article
# _______________________________________________________

@shared_task
def get_send_email():
    artilce = Article.objects.filter(is_active=False)
    if artilce.exists():
        artilce.delete()
        print(f"Inactive articles removed...")
# _______________________________________________________