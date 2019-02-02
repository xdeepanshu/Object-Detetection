from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.utils import timezone

#Using this for running watson detection
from django.db.models.signals import post_save
from django.dispatch import receiver
#For calling watson rpc 
from nameko.standalone.rpc import ClusterRpcProxy
from django.conf import settings #for config variable
import json


class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(default=timezone.now)
    image = CloudinaryField('image')
    watson_response = models.TextField(max_length=10000, editable=True)

    def __str__(self):
        try:
            time = self.create_time
        except AttributeError:
            time = ''
        return "Photo created on <%s>" % (time)
  


@receiver(post_save, sender=Photo)
def photo_handler(sender, **kwargs):
   if kwargs['created']:
       photo_instance = kwargs['instance']
       with ClusterRpcProxy(settings.AMQP_URI) as service:
           result = service.detect.compute(photo_instance.image.url)
           photo_instance.watson_response = json.dumps(result)
           photo_instance.save()
       
