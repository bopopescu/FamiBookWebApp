from django.db import models
from django.contrib import admin
from ..base.baseModel import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name
    class Meta:
        db_table = "categories"   #real db table name

# Display setting on admin page
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields]
    search_fields = ['name']
    ordering =['name']
