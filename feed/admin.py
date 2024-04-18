from django.contrib import admin
from feed.models import *
# Register your models here.

class ImagesInline(admin.StackedInline):
    model=Image
    extra=3

@admin.register(Feed)
class FeedsAdmin(admin.ModelAdmin):
    inlines = (ImagesInline, )
    list_display = ('title','user' ,'description', 'created_at','tag_list')
    prepopulated_fields = {'slug': ('title',)} 

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return ', '.join(o.name for o in obj.tags.all())

@admin.register(Image)
class ImagesAdmin(admin.ModelAdmin):
    list_display=('image_url',)