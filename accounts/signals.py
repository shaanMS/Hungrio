from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Student)
def student_saved(sender, instance, created, **kwargs):
    if created:
        print("New student added:", instance.id)