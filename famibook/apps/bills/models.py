from django.db import models
from django.contrib import admin
from ..categories.models import Category
from ..daybooks.models import Daybook
from ..base.baseModel import BaseModel


class Bill(BaseModel):
    name = models.CharField(max_length=20)
    type = models.IntegerField()  # 0=expense 1=income
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField()
    note = models.TextField(max_length=20)
    category = models.ForeignKey(Category, related_name='bills', on_delete=models.SET_NULL, blank=True, null=True)
    daybook = models.ForeignKey(Daybook, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "bills"  # real db table name


# Display setting on admin page
@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'amount', 'date',
                    'note', 'category', 'daybook', 'created_at', 'updated_at']
    search_fields = ['name']
    ordering = ['name']
    list_display_links = ['name']
    list_filter = ('id',)
