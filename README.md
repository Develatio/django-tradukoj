![PyPI](https://img.shields.io/pypi/v/django-tradukoj.svg)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
![t](https://img.shields.io/badge/status-stable-green.svg)

# Tradukoj

Tradujok is a django db-based translation system with IETF's BCP 47 standard support
and django-rest-framework serializers.

Tradukoj can be integrated with common js i18n libs thanks to his JSON tree generation feature.

This app is maintained and internally used by Develatio Technologies.

## Requierements

* Python: >= 3.6

* Django: >= 2.1, 2.2

## Features

* Namespaces to separate projects or big sections of your app
* JSON tree generation with your translations
* django-rest-framework urls/views/serializers
* django-rest-framework fields to be used in serializers
* Fallback translation for drf fields
* Translate model fields
* Languaje detection endpoint
* RTL - LTR support
* PO files Import/Export
* Public/Private translations isolation

## Quick start

1.  Install `pip install django-tradukoj`

2. Add "tradukoj" to INSTALLED_APPS:

```
INSTALLED_APPS = {
    ...
    'tradukoj'
}
```

3. Include the tradukoj URLconf in urls.py: `url(r'^tradukoj/', include('tradukoj.urls'))`

4. Run `python manage.py migrate` to create db records.


## Translate model fields

Usage of `OneToOneTradukojField`:

```
from tradukoj.fields import OneToOneTradukojField

class MyModel(models.Model):
    name = OneToOneTradukojField(null=True, blank=True, verbose_name='Name')

```

## Handle translations

### Automatic key generation:

```
>>> from tradukoj.models import TranslationKey
>>> from myapp.models import MyModel

>>> instance = MyModel()
>>> # This creates a translatable key with automatically generated name
>>> instance.name = TranslationKey(init_namespace='mynamespace', public=True)
>>> instance.name
<TranslationKey: mynamespace.myapp_mymodel_name_0def4d78080144cdbc96302842935192>

>>> # This will add a translation for es-ES to instance.name
>>> # A record with 'es-ES' into tradukoj.models.BCP47 will be created if it
>>> # does not exist.
>>> instance.name.translate('es-ES', 'mi nombre')

>>> # Access translations:
>>> instance.name.translations.all()
<QuerySet [<Translation: (es-ES - español (Spanish)) mynamespace.myapp_mymodel_name_0def4d78080144cdbc96302842935192 => mi nombre>]>

>>> instance.name.translations.get(bcp47__langtag='es-ES')
<Translation: (es-ES - español (Spanish)) test.medicalscience_specialties_name_0def4d78080144cdbc96302842935192 => mi nombre>

>>> instance.name.translations.get(bcp47__langtag='es-ES').str_translation()
'mi nombre'

```


## Custom key name:

If you dont specify a key for translation, a random one will be generated. To
specify a key, you should pass it as argument to `TranslationKey`:

```
>>> instance.name = TranslationKey(init_namespace='test', text='A translatable string', public=True)
>>> instance.name
<TranslationKey: test.A translatable string>
>>> instance.name.save()
>>> instance.name.translate('es-ES', 'Una cadena traducible')
>>> instance.name.translations.all()
<QuerySet [<Translation: (es-ES - español (Spanish)) test.A translatable string => Una cadena traducible>]>
```


## JSON tree of translations

If you are planning to use json tree feature of tradukoj, remember that a dot in
key are handled as subobject.

```
TranslationKey(init_namespace='project', text='home.title', public=True)
TranslationKey(init_namespace='project', text='home.subtitle', public=True)
```

results into this json object:
```
{
    es-ES: {
        project: {
            home: {
                title: 'Bienvenido',
                subtitle: 'Secciones'
            }
        }
    },
    en-US: {
        project: {
            home: {
                title: 'Welcome',
                subtitle: 'Sections'
            }
        }
    }
}
```


## API REST Endpoints

* Languaje detection: `YOUR_API_URL/tradukoj/bestlangtag/`
Asking from `es-ES;en` (spanish-Spain,english) a web with only
`es-MX` (spanish-Mexico) lang:

```
[
    {
        "langtag": "es-MX",
        "score":92,
        "accept_lang": "es-es"
    },
    {
        "langtag": "es-MX",
        "score": 92,
        "accept_lang":"es"
    },
    {
        "langtag":"en",
        "score":100,
        "accept_lang":"en"
    }
]
```

* Available langs: `YOUR_API_URL/tradukoj/available/`
```
{
    "count": 28,
    "next": null,
    "previous": null,
    "results": [
        {"langtag":"en-EN","name":"English (English)","best_match_score":92,"default":false,"direction":0},
        {"langtag":"es-MX","name":"español (Spanish)","best_match_score":92,"default":false,"direction":0},
        {"langtag":"en-US","name":"English (English)","best_match_score":98,"default":false,"direction":0},
        {"langtag":"ar-LB","name":"العربية (Arabic)","best_match_score":0,"default":false,"direction":1},
        {"langtag":"fr-FR","name":"français (French)","best_match_score":0,"default":false,"direction":0},
        {"langtag":"pt-PT","name":"português (Portuguese)","best_match_score":0,"default":false,"direction":0},
        {"langtag":"ru-RU","name":"русский (Russian)","best_match_score":0,"default":false,"direction":0},
        {"langtag":"de-DE","name":"Deutsch (German)","best_match_score":0,"default":false,"direction":0},
        {"langtag":"it-IT","name":"italiano (Italian)","best_match_score":0,"default":false,"direction":0},
        {"langtag":"hu-HU","name":"magyar (Hungarian)","best_match_score":0,"default":false,"direction":0},
        {"langtag":"cs-CZ","name":"čeština (Czech)","best_match_score":0,"default":false,"direction":0},
        {"langtag":"zh-CN","name":"中文 (Chinese)","best_match_score":0,"default":false,"direction":0},
        {"langtag":"vi-VN","name":"Tiếng Việt (Vietnamese)","best_match_score":0,"default":false,"direction":0},
        {"langtag":"hi-IN","name":"हिन्दी (Hindi)","best_match_score":0,"default":false,"direction":0},
        {"langtag":"uk_UA","name":"українська (Ukrainian)","best_match_score":0,"default":false,"direction":0},
        {"langtag":"hy_AM","name":"հայերեն (Armenian)","best_match_score":0,"default":false,"direction":0},
        {"langtag":"be_BY","name":"беларуская (Belarusian)","best_match_score":0,"default":false,"direction":0},
        {"langtag":"bg_BG","name":"български (Bulgarian)","best_match_score":0,"default":false,"direction":0},
        {"langtag":"km_KH","name":"ខ្មែរ (Khmer)","best_match_score":84,"default":false,"direction":0},
        {"langtag":"et_EE","name":"eesti (Estonian)","best_match_score":0,"default":false,"direction":0},
        {"langtag":"lv_LV","name":"latviešu (Latvian)","best_match_score":0,"default":false,"direction":0},
        {"langtag":"pl_PL","name":"polski (Polish)","best_match_score":0,"default":false,"direction":0},
        {"langtag":"ro_RO","name":"română (Romanian)","best_match_score":0,"default":false,"direction":0},
        {"langtag":"uz_Latn","name":"o‘zbek (Uzbek)","best_match_score":0,"default":false,"direction":0},
        {"langtag":"tr_TR","name":"Türkçe (Turkish)","best_match_score":0,"default":false,"direction":0},
        {"langtag":"th_TH","name":"ไทย (Thai)","best_match_score":0,"default":false,"direction":0},
        {"langtag":"zh_TW","name":"中文 (Chinese)","best_match_score":0,"default":false,"direction":0},
        {"langtag":"az_AZ","name":"azərbaycan (Azerbaijani)","best_match_score":0,"default":false,"direction":0},
    ]
}
```

* Get all public translations list: `YOUR_API_URL/tradukoj/public/`
* Get all private translations list: `YOUR_API_URL/tradukoj/private/`
* Get plain JSON of all public translations: `YOUR_API_URL/tradukoj/public/plain/`
* Get plain JSON of all private translations: `YOUR_API_URL/tradukoj/private/plain/`
* Get filtered public translations: `YOUR_API_URL/tradukoj/public/plain/?bcp47__langtag=es&key__namespace__text=mynamespace`
* Get filtered private translations: `YOUR_API_URL/tradukoj/public/plain/?bcp47__langtag=es&key__namespace__text=mynamespace`


## Django Rest Framework, Tradukoj Field.

To handle a model translatable field into your drf serializers, `TradukojSerializedField`

```
from tradukoj.drf_fields import TradukojSerializedField

class MySerializer(serializers.ModelSerializer):
    name = TradukojSerializedField(read_only=True, fallback_langtag='en-US')

    class Meta:
        model = MyModel
        exclude = ('id', )

```

This will give you a JSON like:

```
{
    name: {
        'fallback': 'Welcome',
        'text': 'mykey',
        'translations': {
            'es-ES': 'Bienvenido',
            'en-US': 'Welcome'
        }
    }
}
```


## Command line tools

### Generate .po file
```
usage: manage.py generate_pofile [-h] --langtag LANGTAG --output OUTPUT
                                 --namespace NAMESPACE --reference_langtag
                                 REFERENCE_LANGTAG [--version] [-v {0,1,2,3}]
                                 [--settings SETTINGS]
                                 [--pythonpath PYTHONPATH] [--traceback]
                                 [--no-color] [--force-color]

Generate a .po file of langtag

optional arguments:
  -h, --help            show this help message and exit
  --langtag LANGTAG     tag used in BCP47
  --output OUTPUT       output file
  --namespace NAMESPACE
                        namespace of translations
  --reference_langtag REFERENCE_LANGTAG
                        translated text used in comments to help translator
                        team
  --version             show program's version number and exit
  -v {0,1,2,3}, --verbosity {0,1,2,3}
                        Verbosity level; 0=minimal output, 1=normal output,
                        2=verbose output, 3=very verbose output
  --settings SETTINGS   The Python path to a settings module, e.g.
                        "myproject.settings.main". If this isn't provided, the
                        DJANGO_SETTINGS_MODULE environment variable will be
                        used.
  --pythonpath PYTHONPATH
                        A directory to add to the Python path, e.g.
                        "/home/djangoprojects/myproject".
  --traceback           Raise on CommandError exceptions
  --no-color            Don't colorize the command output.
  --force-color         Force colorization of the command output.
```

Generate a .po file of `es-ES` and put `en-US` translations as a commentary of
every `msgid`:

`python manage.py generate_pofile --langtag es-ES --output ./pofile.po --namespace mynamespace --reference_langtag en-US`


### Destroy keys not in a .po file:

This will destroy those keys not in a .po file and related translations.

```
usage: manage.py destroy_dbkeys_not_in_pofile [-h] --pofile POFILE --namespace
                                              NAMESPACE [--safe] [--version]
                                              [-v {0,1,2,3}]
                                              [--settings SETTINGS]
                                              [--pythonpath PYTHONPATH]
                                              [--traceback] [--no-color]
                                              [--force-color]

Remove those translations key in DB that does not exists in a given pofile

optional arguments:
  -h, --help            show this help message and exit
  --pofile POFILE       The pofile
  --namespace NAMESPACE
                        The namespace
  --safe                Show those keys that should be deleted but do not
                        commit delete command on db
  --version             show program's version number and exit
  -v {0,1,2,3}, --verbosity {0,1,2,3}
                        Verbosity level; 0=minimal output, 1=normal output,
                        2=verbose output, 3=very verbose output
  --settings SETTINGS   The Python path to a settings module, e.g.
                        "myproject.settings.main". If this isn't provided, the
                        DJANGO_SETTINGS_MODULE environment variable will be
                        used.
  --pythonpath PYTHONPATH
                        A directory to add to the Python path, e.g.
                        "/home/djangoprojects/myproject".
  --traceback           Raise on CommandError exceptions
  --no-color            Don't colorize the command output.
  --force-color         Force colorization of the command output.
```


### Show incompatible keys when use JSON tree generation feature

If you are planning to use JSON tree generation, some keys will be incompatible
with this scheme:

* namespace.section.title = 'test'
* namespace.section = 'test'

to detect those incompatibility, use `show_incompatible_tree_key` command:

```
usage: manage.py show_incompatible_tree_key [-h] [--pofile POFILE] [--version]
                                            [-v {0,1,2,3}]
                                            [--settings SETTINGS]
                                            [--pythonpath PYTHONPATH]
                                            [--traceback] [--no-color]
                                            [--force-color]

Show incompatible Translation Key for plain tree generation

optional arguments:
  -h, --help            show this help message and exit
  --pofile POFILE       Test pofile instead database
  --version             show program's version number and exit
  -v {0,1,2,3}, --verbosity {0,1,2,3}
                        Verbosity level; 0=minimal output, 1=normal output,
                        2=verbose output, 3=very verbose output
  --settings SETTINGS   The Python path to a settings module, e.g.
                        "myproject.settings.main". If this isn't provided, the
                        DJANGO_SETTINGS_MODULE environment variable will be
                        used.
  --pythonpath PYTHONPATH
                        A directory to add to the Python path, e.g.
                        "/home/djangoprojects/myproject".
  --traceback           Raise on CommandError exceptions
  --no-color            Don't colorize the command output.
  --force-color         Force colorization of the command output.
```

### Load .po files

Importing `tradukoj.admin` models into your admin, will give you some features
like importing .po files.

```
from tradukoj import models


class TranslationKeyAdmin(admin.ModelAdmin):
    search_fields = ('text',)

class TranslationAdmin(admin.ModelAdmin):
    search_fields = ('key__text',)


admin.site.register(models.TranslationKey, TranslationKeyAdmin)
admin.site.register(models.GetTextFile)
admin.site.register(models.Namespace)
admin.site.register(models.Translation, TranslationAdmin)
admin.site.register(models.BCP47)

```


### Vue.js: Translate fields POC

Assuming that you are storing your current languaje tag in `store.state.i18n.active_langtag`,
use this POC vuejs code:

create a `plugins/tradukoj-translate.js` with this content:

```
import store from "../store";

const TradukojTranslatable = {
  install(Vue) {
    Vue.mixin({
      methods: {
        $tradukojTranslate(translatable) {
          if (!translatable) {
            return "";
          }

          if (
            translatable.translations &&
            translatable.translations[store.state.i18n.active_langtag]
          ) {
            return translatable.translations[
              store.state.i18n.active_langtag
            ];
          }

          if (translatable.fallback) {
            return translatable.fallback;
          }

          return "";
        }
      }
    });
  }
};
export default TradukojTranslatable;
```

Register globally:

```
import TradukojTranslatable from "@/plugins/tradukoj-translatable";
Vue.use(TradukojTranslatable);
```

Use in component:

```
<template>
  <div>
    <p>{{ $tradukojTranslate(mymodel.name) }}</p>
  </div>
</template>
[...]
```

Once you change the value of `store.state.i18n.active_langtag`, the translations will be
automatically updated to current selected lang.
