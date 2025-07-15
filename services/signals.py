from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=Order)
def send_order_status_email(sender, instance, created, **kwargs):
    if not created:
        subject = f'تحديث حالة طلبك رقم {instance.id}'
        message = f'تم تحديث حالة طلبك إلى: {instance.get_status_display()}.\n\nشكراً لاستخدامك موقعنا!'
        recipient = instance.user.email
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])
