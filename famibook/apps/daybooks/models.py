from django.db import models
from django.contrib import admin
from ..base.baseModel import BaseModel

class Daybook(BaseModel): #models.Model):
    name = models.CharField(max_length=80)
    def __str__(self):
        return self.name
    class Meta:
        db_table = "daybooks"   #real db table name

# Display setting on admin page
@admin.register(Daybook)
class DaybookAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Daybook._meta.fields]
    search_fields = ['name']
    ordering =['name']
