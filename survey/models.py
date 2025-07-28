from django.db import models

class SurveyEntry(models.Model):
    state = models.CharField(max_length=100)
    segment_id = models.CharField(max_length=100)
    route_id = models.CharField(max_length=100)
    category = models.CharField(max_length=200)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)