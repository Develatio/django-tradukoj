# -*- coding: utf-8 -*-
from langcodes import best_match
from django.utils.translation import ugettext_lazy as _
from django.utils.translation.trans_real import parse_accept_lang_header
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Translation, BCP47
from .serializers import (TranslationSerializer, BCP47Serializer)


class PublicTranslationList(generics.ListAPIView):
    """Public endpoint to list translations"""
    queryset = Translation.objects.filter(
        key__public=True,
        bcp47__enabled=True,
    )
    serializer_class = TranslationSerializer
    filterset_fields = ('bcp47__langtag', 'key__text', 'key__namespace__text')
    permission_classes = (AllowAny, )


# class PublicTranslationRawList(APIView):
#     """Public endpoint to list translations in a plain way.
#
#     Return a big json:
#     {
#         'langtag': {
#             'key': 'translation',
#             'key2': 'translation2'
#         },
#         'langtag2': {
#             'key': 'translation',
#             'key2': 'translation2'
#         }
#     }
#
#     """
#     permission_classes = ()
#
#     def get(self, request, format=None):
#         # import pdb; pdb.set_trace()
#         data = Translation.get_cached_public_translations()
#         return Response(data)
#


class PublicTranslationRawList(generics.ListAPIView):
    """Public endpoint to list translations in a plain way.

    Return a big json:
    {
        'langtag': {
            'namespace': {
                'key': 'translation',
                'key2': 'translation2'
            }
        }
    }

    Note: ignore swagger model and result reference, it lies :)

    """
    serializer_class = TranslationSerializer
    http_method_names = [u'get']
    pagination_class = None
    paginate_by = None
    # filter_backends = None
    filterset_fields = (
        'bcp47__langtag',
        'key__namespace__text',
    )
    permission_classes = (AllowAny, )

    def list(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        langtag = request.query_params.get('bcp47__langtag')
        namespace = request.query_params.get('key__namespace__text')
        if langtag is None:
            raise ValidationError({'bcp47__lang': _('This field is required.')}, code='required')
        if namespace is None:
            raise ValidationError({'key__namespace__text': _('This field is required.')}, code='required')
        data = Translation.get_cached_public_translations(langtag, namespace)
        return Response(data)

    def get_queryset(self):
        return Translation.objects.all()


class PrivateTranslationRawList(generics.ListAPIView):
    """Private endpoint to list translations in a plain way.

    Return a big json:
    {
        'langtag': {
            'namespace': {
                'key': 'translation',
                'key2': 'translation2'
            }
        }
    }

    Note: ignore swagger model and result reference, it lies :)

    """
    serializer_class = TranslationSerializer
    http_method_names = [u'get']
    pagination_class = None
    paginate_by = None
    # filter_backends = None
    filterset_fields = (
        'bcp47__langtag',
        'key__namespace__text',
    )
    permission_classes = (AllowAny, )

    def list(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        langtag = request.query_params.get('bcp47__langtag')
        namespace = request.query_params.get('key__namespace__text')
        if langtag is None:
            raise ValidationError({'bcp47__lang': _('This field is required.')}, code='required')
        if namespace is None:
            raise ValidationError({'key__namespace__text': _('This field is required.')}, code='required')
        data = Translation.get_cached_private_translations(langtag, namespace)
        return Response(data)

    def get_queryset(self):
        return Translation.objects.all()


class PublicTranslationRetrieve(generics.RetrieveAPIView):
    """Public endpoint to retrieve single translation"""
    queryset = Translation.objects.filter(key__public=True, bcp47__enabled=True)
    serializer_class = TranslationSerializer
    lookup_field = 'key__text'
    lookup_value_regex = '[-\w]+'
    permission_classes = (AllowAny, )

    def get_queryset(self):
        return Translation.objects.filter(
            key__public=True,
            bcp47__enabled=True,
            bcp47__langtag=self.kwargs.get('langtag'),
        )


class PrivateTranslationList(generics.ListAPIView):
    """Private (auth requiered) endpoint to list translations"""
    queryset = Translation.objects.filter(bcp47__enabled=True)
    serializer_class = TranslationSerializer
    filterset_fields = ('bcp47__langtag', 'key__text', 'key__namespace__text')
    permission_classes = (IsAuthenticated, )


class PrivateTranslationRetrieve(generics.RetrieveAPIView):
    """Private (auth requiered) endpoint retrieve single translation"""
    queryset = Translation.objects.filter(bcp47__enabled=True)
    serializer_class = TranslationSerializer
    lookup_field = 'key__text'
    lookup_value_regex = '[-\w]+'
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Translation.objects.filter(
            bcp47__enabled=True,
            bcp47__langtag=self.kwargs.get('langtag'),
        )


class EnabledLangs(generics.ListAPIView):
    """Public endpoint to list all availabe localizations"""
    queryset = BCP47.objects.filter(enabled=True)
    serializer_class = BCP47Serializer
    permission_classes = (AllowAny, )


class BestlangtagList(APIView):
    """An scored list with best available langtag.

    Match HTTP_ACCEPT_LANGUAGE with available langtags in db and compare
    using langcodes library.

    Returns:
        dict: a list with langtag, score and accept_lang feedback.
    """

    permission_classes = (AllowAny, )

    # TODO: add default boolean firld to langs and order by default
    # pylint: disable=unused-argument
    def get(self, request, **kwargs):
        enabledlangs = []
        for bcp47instance in BCP47.objects.filter(enabled=True):
            enabledlangs.append(bcp47instance.langtag)

        accept = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
        data = []
        for accept_lang, _ in parse_accept_lang_header(accept):
            match = best_match(accept_lang, enabledlangs)
            data.append({
                'langtag': match[0],
                'score': match[1],
                'accept_lang': accept_lang,
            })
        # results = BestlangtagSerializer(data, many=True).data
        return Response(data)
