from rest_framework.fields import Field, empty
from rest_framework.exceptions import NotFound
from tradukoj.models import TranslationKey
from tradukoj.serializers import TranslationKeyWithTranslationsSerializer


class TradukojKeyTextField(Field):
    def to_internal_value(self, data):
        try:
            key = TranslationKey.objects.get(text=data)
        except TranslationKey.DoesNotExist:
            raise NotFound(f"key text for {self.field_name} not found")

        return key

    def to_representation(self, value):
        if value:
            return value.text
        return None


class TradukojSerializedField(TranslationKeyWithTranslationsSerializer):

    fallback_langtag = None

    def __init__(self, instance=None, data=empty, **kwargs):
        if 'fallback_langtag' in kwargs:
            self.fallback_langtag = kwargs['fallback_langtag']
            del kwargs['fallback_langtag']
        super(TradukojSerializedField, self).__init__(instance, data, **kwargs)

    def to_representation(self, instance):
        if not instance:
            return {}

        representation = {'text': instance.text, 'translations': {}}
        if self.fallback_langtag:
            representation['fallback'] = None
        for translation in instance.translations.select_related('bcp47').all():
            representation['translations'][
                translation.bcp47.langtag] = translation.str_translation()
            if (self.fallback_langtag
                    and translation.bcp47.langtag == self.fallback_langtag):
                representation['fallback'] = translation.str_translation()

        return representation
