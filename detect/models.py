from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.utils import timezone

class Photo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user")
    create_time = models.DateTimeField(default=timezone.now)
    title = models.CharField("Title (optional)", max_length=200, blank=True)
    image = CloudinaryField('image')

    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
        return "Photo <%s:%s>" % (self.title, public_id)
