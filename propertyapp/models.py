from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

class User(models.Model):
    username = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.username


class Property(models.Model):

    FUR_CHOICES = (
    (1, ("Furnished")),
    (2, ("Semi-Furnished")),
    (3, ("Unfurnished")),
    )
    gender = (
    (1, ("Female")),
    (2, ("Male")),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rent = models.IntegerField()
    prop_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    desc = models.TextField()
    furnishing = models.IntegerField(choices=FUR_CHOICES, default=1)
    amenities = models.CharField(max_length=256, default='RO, Geyser')
    gender = models.IntegerField(choices=gender, default=1)
    

    def __str__(self) -> str:
        return self.prop_name
    

class Image(models.Model):
    image = models.ImageField(storage=S3Boto3Storage(), default="www.google.com")
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    # def __str__(self) -> str:
    #     return self.image
