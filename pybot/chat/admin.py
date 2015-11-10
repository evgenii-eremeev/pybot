from django.contrib import admin
from .models import Query, Notes


# Register your models here.
class QueryAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'user', 'date']
    list_filter = ['user']


class NotesAdmin(admin.ModelAdmin):
    list_display = ['note', 'user', 'date']
    list_filter = ['user']

admin.site.register(Query, QueryAdmin)
admin.site.register(Notes, NotesAdmin)