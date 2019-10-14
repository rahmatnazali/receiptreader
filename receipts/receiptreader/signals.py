from .google_vision_api import GoogleVisionApi
#
from django.db.models.signals import post_save
#

# def document_save(sender, instance, **kwargs):
#   import pdb; pdb.set_trace()
#   print("Instance = ", instance)
#   googlevision = GoogleVisionApi()
#   returnedjson = googlevision.ocr_image(instance)
#   print(returnedjson)
# post_save.connect(document_save, sender=Document)

#def rawjson_save(sender, instance, **kwargs):


from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#
from cmdbox.profiles.models import Profile
#



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
