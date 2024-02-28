from django.contrib import admin
from .models import Note



admin.site.register(Note) 
# admin.site.register(BlogPost) 

"""
# Customizing admin interface:
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('field1', 'field2')  # Fields to display in the model list page
    search_fields = ['field1', 'field2']  # Fields to search in the admin list page

# Register the model with customized admin options
admin.site.register(MyModel, MyModelAdmin)
"""