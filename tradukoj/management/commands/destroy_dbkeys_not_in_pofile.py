import polib
from django.core.management.base import BaseCommand
from tradukoj.models import TranslationKey


class Command(BaseCommand):
    # pylint: disable=C0301
    help = 'Remove those translations key in DB that does not exists in a given pofile'
    exitcode = 0
    data = None

    def add_arguments(self, parser):
        parser.add_argument(
            '--pofile',
            dest='pofile',
            required=True,
            help='The pofile',
        )

        parser.add_argument(
            '--namespace',
            dest='namespace',
            required=True,
            help='The namespace',
        )

        parser.add_argument(
            '--safe',
            dest='safe',
            required=False,
            help=
            'Show those keys that should be deleted but do not commit delete command on db',
            action="store_true",
        )

    def handle(self, *args, **options):
        po_file = polib.pofile(options['pofile'])
        safe_advisory = ""

        if options["safe"]:
            safe_advisory = "(Not really because --safe arg)"

        for translationkey in TranslationKey.objects.filter(
                namespace__text=options['namespace']):
            if not po_file.find(translationkey.text):
                self.stdout.write(
                    f"Delete {safe_advisory} {translationkey.text}")
                if not options["safe"]:
                    translationkey.delete()

        self.stdout.write(self.style.SUCCESS('DONE'))
