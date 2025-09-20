import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import PaymentRecord


def delete_file_if_needed(instance, old_file):
    if old_file and old_file != instance.proof_of_payment:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(pre_save, sender=PaymentRecord)
def auto_delete_old_file_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return  # Skip for new records

    try:
        old_record = PaymentRecord.objects.get(pk=instance.pk)
    except PaymentRecord.DoesNotExist:
        return

    delete_file_if_needed(instance, old_record.proof_of_payment)


@receiver(post_delete, sender=PaymentRecord)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.proof_of_payment:
        if os.path.isfile(instance.proof_of_payment.path):
            os.remove(instance.proof_of_payment.path)
