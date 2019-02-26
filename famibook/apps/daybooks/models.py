from django.db import models
from django.utils import timezone

class Daybook(models.Model):
    name = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Daybook, self).save(*args, **kwargs)
    def __str__(self):
        return self.name
    class Meta:
        db_table = "daybooks"   #real db table name
