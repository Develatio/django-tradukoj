from django.contrib import admin
from tradukoj import models


class TranslationKeyAdmin(admin.ModelAdmin):
    search_fields = ('text', )
    list_display = ('__str__', )


class TranslationAdmin(admin.ModelAdmin):
    search_fields = (
        'key__text',
        'small',
        'largue',
    )
    raw_id_fields = ('key', )


admin.site.register(models.TranslationKey, TranslationKeyAdmin)
admin.site.register(models.GetTextFile)
admin.site.register(models.Namespace)
admin.site.register(models.Translation, TranslationAdmin)
admin.site.register(models.BCP47)
