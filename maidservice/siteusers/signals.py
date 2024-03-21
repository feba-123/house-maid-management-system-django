from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone
from .models import Order, Notification



# @receiver(post_save, sender=Order)
# def notifications(sender, instance, created, **kwargs):
#     if created:
#
#         get_booking = Order.objects.filter(expiring_date=thrushold)
#         if get_booking:
#             message = "a new booking found"
#             Notification.objects.create(message=message)
#
#


@receiver(post_save, sender=Order)
def notify_admin_on_booking(sender, instance, created, **kwargs):
    if created:
        message = "New booking: booked a maid."
        notify = Notification.objects.create(message=message)
        notify.save()