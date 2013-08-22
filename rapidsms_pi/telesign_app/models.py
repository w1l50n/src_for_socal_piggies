from django.db import models

class PhoneID(models.Model):

    reference_id = models.CharField(max_length=32, db_index=True)
    phone_number = models.CharField(max_length=16, db_index=True)
    carrier = models.CharField(max_length=128, null=True)
    phone_type = models.CharField(max_length=32, null=True)
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    iso2 = models.CharField(max_length=2, null=True)
    state = models.CharField(max_length=2, null=True)
    zip_code = models.IntegerField(null=True)
    raw_json = models.TextField(null=True)
