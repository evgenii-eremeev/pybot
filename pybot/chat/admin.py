from django.contrib import admin
from .models import Query


# Register your models here.
class QueryAdmin(admin.ModelAdmin):
    list_display = ['date', 'user', 'question', 'answer']
    list_filter = ['user']


admin.site.register(Query, QueryAdmin)