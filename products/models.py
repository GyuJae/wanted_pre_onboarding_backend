from django.db import models
from core import models as core_models

# Create your models here.
class Product(core_models.TimeStampedModel):

    """Product Model Definition"""
    
    title = models.CharField(max_length=140)
    publisher_name = models.CharField(max_length=140)
    description = models.TextField()
    target_amount = models.IntegerField()
    funding_end_date = models.DateField()
    one_time_funding_amount = models.IntegerField()

    def __str__(self):
        return self.title
