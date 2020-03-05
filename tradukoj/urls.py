from django.conf.urls import url
from . import classviews

urlpatterns = [
    # LCRUD insurances
    url(r'^public/$', classviews.PublicTranslationList.as_view(),
        name="public_tradukoj_translation_list"),

    url(
        r'^public/(?P<langtag>[-\w]+)/(?P<namespace>[-\w]+)/(?P<key__text>.*)/$',
        classviews.PublicTranslationRetrieve.as_view(),
        name="public_tradukoj_translation_retrieve",
    ),


    url(r'^public/plain/$', classviews.PublicTranslationRawList.as_view(
    ), name="public_tradukoj_translation_plain_list"),


    url(r'^private/plain/$', classviews.PrivateTranslationRawList.as_view(
    ), name="private_tradukoj_translation_plain_list"),


    url(r'^private/$', classviews.PrivateTranslationList.as_view(),
        name="private_tradukoj_translation_list"),


    url(
        r'^private/(?P<langtag>[-\w]+)/(?P<namespace>[-\w]+)/(?P<key__text>.*)/$',
        classviews.PrivateTranslationRetrieve.as_view(),
        name="private_tradukoj_translation_retrieve",
    ),


    url(r'^available/$', classviews.EnabledLangs.as_view(),
        name="available_tradukoj_translation_list"),


    url(r'^bestlangtag/$', classviews.BestlangtagList.as_view(),
        name="bestlangtag_tradukoj_translation_list"),

]
