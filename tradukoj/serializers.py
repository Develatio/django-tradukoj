from langcodes import best_match
from django.utils.translation.trans_real import parse_accept_lang_header
from rest_framework import serializers
from .models import Translation, BCP47, TranslationKey


class BCP47Serializer(serializers.ModelSerializer):
    best_match_score = serializers.SerializerMethodField()

    class Meta:
        model = BCP47
        fields = ('langtag', 'name', 'best_match_score', 'default', 'direction')

    # TODO: Implement MaxMind Geo-IP location
    def get_best_match_score(self, obj):
        # best_match(accept_lang, enabledlangs, min_score=50)
        accept_header = self.context['request'].META.get('HTTP_ACCEPT_LANGUAGE', '')
        accept_lang = []
        # Read https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#internationalization-in-python-code
        for accepted, _q in parse_accept_lang_header(accept_header):
            accept_lang.append(accepted)

        # get best accepted match for this tag
        best = best_match(obj.langtag, accept_lang, min_score=50)
        # get the index of matched lang
        try:
            idx = accept_lang.index(best[0])
        except ValueError:
            return 0

        # return the score extracting the index, so the matched position at index
        # zero and score 100 will return 100. matched position at index 1 and
        # score 100 will return 99
        return best[1] - idx


class TranslationKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslationKey
        fields = (
            'text',
            'namespace',
        )


class TranslationKeyWithTranslationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslationKey
        fields = (
            'text',
            'namespace',
            'translations',
        )


class TranslationSerializer(serializers.ModelSerializer):
    translation = serializers.SerializerMethodField()
    key = TranslationKeySerializer()
    bcp47 = BCP47Serializer()

    class Meta:
        model = Translation
        fields = (
            'id',
            'key',
            'bcp47',
            'is_largue',
            'small',
            'largue',
            'translation',
        )

    def get_translation(self, obj):
        return obj.str_translation()


class BestlangtagSerializer(serializers.Serializer):
    langtag = serializers.CharField()
    accept_lang = serializers.CharField()
    score = serializers.CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
