from django.contrib import admin

# Register your models here.
from . import models


from mptt.admin import MPTTModelAdmin


class CustomMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 10

    list_display=(
        'name',
        'slug',
        'id',
        'level',
        'parent',
        'lft',
        'rght'
        # ...more fields if you feel like it...
    )


admin.site.register(models.Category, CustomMPTTModelAdmin)
# admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.Tag)


class ArticleAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
    #    super(ArticleAdmin, self).save_model(request, obj, form, change)
        if not change:
            # the object is being created, so set the user
            obj.author = request.user
        obj.save()


admin.site.register(models.Article, ArticleAdmin)