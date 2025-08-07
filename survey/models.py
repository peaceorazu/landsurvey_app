from django.db import models

class SurveyEntry(models.Model):
    state = models.CharField(max_length=100)
    segment_id = models.CharField(max_length=100)
    route_id = models.CharField(max_length=100)
    category = models.CharField(max_length=200)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.category} - {self.value} (at {self.timestamp})"