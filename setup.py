import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='django-tradukoj',
    python_requires='>=3.6.0',
    version='1.0.1',
    packages=['tradukoj'],
    description='A django IETF\'s BCP 47 DB-based translation system',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Develatio Technologies S.L.',
    author_email='contacto@develat.io',
    url='https://github.com/develatio/django-tradukoj/',
    license='BSD',
    install_requires=['Django>=2.0', 'langcodes >= 1.4.1'])
