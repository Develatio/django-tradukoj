"""
Models definition for IETF's BCP 47 standard.

Used standard: IETF's BCP 47.
Standar RFC: http://www.rfc-editor.org/rfc/rfc5646.txt

For fun links:
https://www.w3.org/International/articles/language-tags/
https://en.wikipedia.org/wiki/IETF_language_tag


from RFC, a langtag is composed by:
langtag       = language
                ["-" script]
                ["-" region]
                *("-" variant)
                *("-" extension)
                ["-" privateuse]
So, there is:
language-extlang-script-region-variant-extension-privateuse
"""
from tempfile import NamedTemporaryFile
from django.db import models
# Future use
# from django.db import DEFAULT_DB_ALIAS, connections
from django.core.cache import cache
from django.utils.translation.trans_real import parse_accept_lang_header
import polib
from langcodes import best_match


def best_langtag_list(accept):
    enabledlangs = []
    for bcp47instance in BCP47.objects.filter(enabled=True):
        enabledlangs.append(bcp47instance.langtag)

    data = []
    for accept_lang, _ in parse_accept_lang_header(accept):
        match = best_match(accept_lang, enabledlangs)
        data.append({
            'langtag': match[0],
            'score': match[1],
            'accept_lang': accept_lang,
        })
    return data


class BCP47(models.Model):
    DIRECTION_LTR = 0
    DIRECTION_RTL = 1
    DIRECTION_CHOICES = (
        (DIRECTION_LTR, 'Left to Right (LTR)'),
        (DIRECTION_RTL, 'Right to Left (RTL)'),
    )

    langtag = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name='IETF BCP 47 langtag')
    name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Lang name')
    enabled = models.BooleanField(default=True)
    # used as fallback
    default = models.BooleanField(default=False)
    direction = models.IntegerField(default=0, choices=DIRECTION_CHOICES)

    def __str__(self):
        return f"{self.langtag} - {self.name}"


class Namespace(models.Model):
    text = models.CharField(
        unique=True,
        max_length=255,
        null=False,
        blank=False,
        verbose_name='text key')

    def __str__(self):
        return self.text


class TranslationKey(models.Model):

    init_namespace = None
    auto_key_text = True

    text = models.CharField(
        max_length=255, null=False, blank=False, verbose_name='text key')

    namespace = models.ForeignKey(
        'Namespace',
        null=False,
        blank=False,
        related_name='translation_keys',
        on_delete=models.CASCADE)
    public = models.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        # create namespace into db on init_namespace set
        if 'init_namespace' in kwargs:
            self.init_namespace = kwargs['init_namespace']
            namespace, _created = Namespace.objects.get_or_create(
                text=kwargs['init_namespace'])

            kwargs['namespace'] = namespace
            del kwargs['init_namespace']

        # parameter to disable auto key text generation
        if 'auto_key_text' in kwargs:
            self.auto_key_text = kwargs['auto_key_text']
            del kwargs['auto_key_text']

        super().__init__(*args, **kwargs)

    def get_init_namespace(self):
        return self.init_namespace

    def translate(self, langtag, translation_text):
        bcp47, created = BCP47.objects.get_or_create(langtag=langtag)
        if created:
            bcp47.enabled = True
            bcp47.save()
        translation, _created = Translation.objects.get_or_create(
            key=self, bcp47=bcp47)
        if len(translation_text) > 255:
            translation.is_largue = True
            translation.largue = translation_text
        else:
            translation.is_largue = False
            translation.small = translation_text

        translation.save()

    def get_translation(self, langtag=None):
        try:
            if not langtag:
                translation = self.translations.get(bcp47__default=True)
                return translation
            translation = self.translations.get(bcp47__langtag=langtag)
            return translation
        except Translation.DoesNotExist:
            return None

    def get_translation_str(self, langtag=None):
        translation = self.get_translation(langtag)
        if not translation:
            return ''
        return translation.str_translation()

    def __str__(self):
        return f"{self.namespace}.{self.text}"

    class Meta:
        unique_together = (
            'namespace',
            'text',
        )


# TODO: update cache on save event
class Translation(models.Model):
    key = models.ForeignKey(
        TranslationKey,
        null=False,
        blank=False,
        related_name='translations',
        on_delete=models.CASCADE)
    bcp47 = models.ForeignKey(
        BCP47,
        null=False,
        blank=False,
        related_name='translations',
        on_delete=models.CASCADE)
    is_largue = models.BooleanField(default=False)
    small = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='small')
    largue = models.TextField(null=True, blank=True, verbose_name='largue')

    class Meta:
        unique_together = (
            'key',
            'bcp47',
        )

    # Future use
    # @staticmethod
    # def database_has_jsonb_agg():
    #     connection = connections[DEFAULT_DB_ALIAS]
    #     return connection.features.has_jsonb_agg

    def str_translation(self):
        if self.is_largue:
            return self.largue
        return self.small

    @staticmethod
    def get_cached_public_translations(langtag, namespace):
        """
        Return a big cached json of all translations.

        This will update cache if needed.

        """

        data = cache.get('tradukoj_pub_tr_{0}_{1}'.format(langtag, namespace))
        if data is None:
            Translation.update_langtag_cache(langtag, namespace)
        return cache.get('tradukoj_pub_tr_{0}_{1}'.format(langtag, namespace))

    @staticmethod
    def get_cached_private_translations(langtag, namespace):
        """
        Return a big cached json of all translations.

        This will update cache if needed.

        """
        data = cache.get('tradukoj_priv_tr_{0}_{1}'.format(langtag, namespace))
        if data is None:
            Translation.update_langtag_cache(langtag, namespace, False)
        return cache.get('tradukoj_priv_tr_{0}_{1}'.format(langtag, namespace))

    @staticmethod
    def update_langtag_cache(langtag, namespace, public=True):
        """Update cache with big json of all translations."""
        data = {langtag: {namespace: {}}}
        queryset = Translation.objects.filter(
            key__namespace__text=namespace,
            bcp47__enabled=True,
            bcp47__langtag=langtag,
        ).annotate(annotate_key_text=models.F('key__text'))

        cache_string = 'tradukoj_priv_tr_{0}_{1}'.format(langtag, namespace)
        if public:
            cache_string = 'tradukoj_pub_tr_{0}_{1}'.format(langtag, namespace)
            queryset = queryset.filter(key__public=True)

        # hacemos foreach por las traducciones
        for translation in queryset:
            if not translation.str_translation():
                continue

            if not translation.str_translation().strip():
                continue

            # si la key de traducción es de tipo login.form.username
            # hacemos split en el punto (.) e iteramos sobre él.
            #
            # _current node contendrá (por referencia) el último nodo creado
            # de este mode, de un string tipo login.form.username vamos creando:
            # data[langtag][namespace]['login'] = {}
            # data[langtag][namespace]['login']['form'] = {}
            # data[langtag][namespace]['login']['form']['username'] = 'traduccion'
            deep = translation.annotate_key_text.split('.')
            _current_node = data[langtag][namespace]
            for i, element in enumerate(deep):
                # en el último elemento dejamos de profundizar y colocamos la traducción
                if i == (len(deep) - 1):
                    # Incongruity key error.
                    # _current_node debe ser un dict,
                    # de lo contrario algo ha ido mal.
                    # Posibles causas:
                    # 1) Existe una key node1.node2 = text y otra
                    #    node1.node2.node3 = text
                    #    con lo cual el algoritmo espera que node1.node2
                    #    sea un dict para añadirle una nueva clave, pero
                    #    se encuentra un string
                    if not isinstance(_current_node, dict):
                        break
                    _current_node[element] = translation.str_translation()
                    break
                if not element in _current_node:
                    _current_node[element] = {}

                # Solución parcial para gestionar
                # el fallo Incongruity key (arriba)
                # Si encuentra un elemento que se espera sea dict y no lo es,
                # sobreescribir como dict.
                # Esto provocará que node1.text2 = "text" se sobreescriba con
                # node1.text2 = {} para poder profundizar en el árbol
                # TODO: buscar cómo gestionar esto en Tradukoj
                # Opción 1: evitar keys node1.node2 si existe node1.node2.node3
                #           mediante validación en modelo
                # Opción 2: devolver un array [{traducciones}, {traducciones}]
                #           donde en el primer dict devolver las traduccionnes
                #           normales node1.node2.node3 y en el segundo dict
                #            devolver node1.node2
                if not isinstance(_current_node[element], dict):
                    _current_node[element] = {}

                # aquí está la magia, la variable _current_node es seteada por referencia
                _current_node = _current_node[element]

        if public:
            return cache.set(cache_string, data)

        return cache.set(cache_string, data)

    def __str__(self):
        if self.is_largue:
            return f"({self.bcp47}) {self.key} => {self.largue}"
        return f"({self.bcp47}) {self.key} => {self.small}"


class GetTextFile(models.Model):
    FILE_TYPE_PO = 0
    FILE_TYPE_MO = 1
    FILE_TYPE_CHOICES = ((FILE_TYPE_PO, 'PO file'), (FILE_TYPE_MO, 'MO file'))

    file = models.FileField(upload_to='uploads/tradukoj')
    file_type = models.IntegerField(default=0, choices=FILE_TYPE_CHOICES)
    bcp47 = models.ForeignKey(
        BCP47,
        null=False,
        blank=False,
        related_name='get_text_files',
        on_delete=models.CASCADE,
        verbose_name='Lang')
    namespace = models.ForeignKey(
        Namespace,
        null=False,
        blank=False,
        related_name='get_text_files',
        on_delete=models.CASCADE)
    last_updated_date = models.DateTimeField(
        db_index=True, auto_now=True, verbose_name='Last updated date')
    done = models.BooleanField(default=False)
    done_with_errors = models.BooleanField(default=False)
    log = models.TextField(
        null=True,
        blank=True,
        max_length=1024,
        verbose_name='Log',
    )

    def process_file(self):
        with NamedTemporaryFile() as tmpfile:
            po_file_content = self.file.open().readlines()
            tmpfile.writelines(po_file_content)
            tmpfile.seek(0)

            gettext_file = polib.pofile(tmpfile.name)
            for entry in gettext_file:
                translation_key, _created = TranslationKey.objects.get_or_create(
                    text=entry.msgid, namespace=self.namespace)

                translation, _created = Translation.objects.get_or_create(
                    key=translation_key, bcp47=self.bcp47)

                if len(entry.msgstr) > 255:
                    translation.is_largue = True
                    translation.largue = entry.msgstr
                    translation.small = None
                else:
                    translation.is_largue = False
                    translation.small = entry.msgstr
                    translation.largue = None

                translation.save()
            tmpfile.close()

    def __str__(self):
        return "{0} {1} {2} ".format(self.bcp47, self.namespace.text,
                                     self.file)
