from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import GetTextFile

@receiver(post_save, sender=GetTextFile)
def fill_total(instance=None, **_kwargs):
    instance.done = False
    if instance.process_file():
        instance.done = True
