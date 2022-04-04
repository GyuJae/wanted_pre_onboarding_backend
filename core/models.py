from django.db import models

class TimeStampedModel(models.Model): 

    """ Time Stamped Model """

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True