import sys
import polib
from django.core.management.base import BaseCommand
from tradukoj.models import Namespace


class Command(BaseCommand):
    # pylint: disable=C0301
    help = 'Show incompatible Translation Key for plain tree generation'
    exitcode = 0
    data = None

    def add_arguments(self, parser):
        parser.add_argument(
            '--pofile',
            dest='pofile',
            required=False,
            help='Test pofile instead database',
        )

    def handle(self, *args, **options):
        if 'pofile' in options:
            po_file = polib.pofile(options['pofile'])
            self.data = {"test": {}}
            for entry in po_file:
                self.test_text(entry.msgid)
            self.stdout.write(self.style.SUCCESS(f"Done {options['pofile']}"))
            sys.exit(self.exitcode)

        for namespace in Namespace.objects.all():
            self.stdout.write(f"Testing {namespace}...")
            self.data = {"test": {}}
            for translationkey in namespace.translation_keys.all():
                self.test_text(translationkey.text)
            self.stdout.write(self.style.SUCCESS(f"Done {namespace} test."))
        sys.exit(self.exitcode)

    def test_text(self, translationkey):
        if not translationkey:
            return
        if not translationkey.strip():
            return
        deep = translationkey.split('.')
        _current_node = self.data['test']
        for i, element in enumerate(deep):
            if i == (len(deep) - 1):
                if not isinstance(_current_node, dict):
                    self.stdout.write(
                        f"Error: The key `{element}` in `{translationkey}` tries to be an object but there are string on this path"
                    )
                    self.exitcode = 1
                    break
                if element in _current_node:
                    self.stdout.write(
                        f"Error: The key `{element}` in `{translationkey}` tries to be an string but there are object on this path"
                    )
                    self.exitcode = 1
                    break
                _current_node[element] = str(translationkey)
                break
            if not element in _current_node:
                _current_node[element] = {}

            if isinstance(_current_node[element], str):
                self.stdout.write(
                    f"Error: The key `{element}` in `{translationkey}` tries to be an object but there are string on this path"
                )
                self.exitcode = 1
                break

            if element not in _current_node:
                _current_node[element] = {}

            _current_node = _current_node[element]
