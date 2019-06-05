import polib
from django.core.management.base import BaseCommand
from tradukoj.models import Translation, TranslationKey


class Command(BaseCommand):
    # pylint: disable=C0301
    help = 'Generate a .po file of langtag'

    def add_arguments(self, parser):

        parser.add_argument(
            '--langtag',
            dest='langtag',
            required=True,
            help='tag used in BCP47',
        )

        parser.add_argument(
            '--output',
            dest='output',
            required=True,
            help='output file',
        )

        parser.add_argument(
            '--namespace',
            dest='namespace',
            required=True,
            help='namespace of translations',
        )

        parser.add_argument(
            '--reference_langtag',
            dest='reference_langtag',
            required=True,
            help='translated text used in comments to help translator team',
        )

    def handle(self, *args, **options):
        langtag = options['langtag']
        output_file = options['output']
        reference_langtag = options['reference_langtag']
        namespace = options['namespace']

        po_object = polib.POFile()
        # TODO: allow configure metadata
        po_object.metadata = {
            'Content-Type': 'text/plain; charset=utf-8',
        }
        for translation_key in TranslationKey.objects.filter(
                namespace__text=namespace):

            translated = ""
            try:
                translation = Translation.objects.get(
                    bcp47__langtag=langtag, key=translation_key)
                translated = translation.str_translation()
            except Translation.DoesNotExist:
                translated = ""

            if not translation_key.text:
                continue

            help_text = ""
            try:
                reference_translation = Translation.objects.get(
                    bcp47__langtag=reference_langtag, key=translation_key)
                help_text = f"i18n {reference_langtag}: {reference_translation.str_translation()}"
            except Translation.DoesNotExist:
                help_text = "i18n {reference_langtag}: "

            if not translated:
                translated = ""
            entry = polib.POEntry(
                msgid=translation_key.text,
                msgstr=translated,
                comment=help_text)
            po_object.append(entry)

        po_object.save(output_file)
