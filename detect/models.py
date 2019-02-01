from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.utils import timezone

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(default=timezone.now)
    image = CloudinaryField('image')
    watson_response = models.TextField(max_length=10000, editable=True)

    def __unicode__(self):
        try:
            public_id = self.user.name
        except AttributeError:
            public_id = ''
        return "Photo <%s>" % (public_id)
