import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='django-tradukoj',
    python_requires='>=3.6.0',
    version='1.0.3',
    packages=find_packages(exclude=['tests*']),
    description='A django IETF\'s BCP 47 DB-based translation system',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Develatio Technologies S.L.',
    author_email='contacto@develat.io',
    url='https://github.com/develatio/django-tradukoj/',
    license='BSD',
    install_requires=['Django>=2.0', 'langcodes >= 1.4.1'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Software Development :: Localization",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)
