from email.policy import default
from django.db import models
from core import models as core_models

# Create your models here.
class Product(core_models.TimeStampedModel):

    """Product Model Definition"""

    title = models.CharField(max_length=140)
    publisher = models.ForeignKey("users.User", on_delete=models.CASCADE)

    description = models.TextField()
    target_amount = models.IntegerField()
    funding_end_date = models.DateField()
    one_time_funding_amount = models.IntegerField()
    total_amount = models.IntegerField(default=0)
    participants_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def publisher_name(self):
        return self.publisher.username

    def d_day(self):

        import datetime

        today = datetime.date.today()
        end_date_split = list(map(int, str(self.funding_end_date).split("-")))
        target_date = datetime.date(
            end_date_split[0], end_date_split[1], end_date_split[2]
        )
        return (target_date - today).days

    def achievment_rate(self):
        return self.total_amount / self.target_amount
