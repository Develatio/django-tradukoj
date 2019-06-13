from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import GetTextFile


@receiver(post_save, sender=GetTextFile)
def process_file(instance=None, **_kwargs):
    instance.done = False
    if instance.process_file():
        instance.done = True
