from setuptools import setup
import json


with open('metadata.json', encoding='utf-8') as fp:
    metadata = json.load(fp)


setup(
    name='lexibank_savelyevturkic',
    version="1.0",
    description=metadata['title'],
    license=metadata.get('license', ''),
    url=metadata.get('url', ''),
    py_modules=['lexibank_savelyevturkic'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'savelyevturkic=lexibank_savelyevturkic:Dataset',
        ],
        'cldfbench.commands': [
            'savelyevturkic=savelyevturkiccommands',
        ]

    },
    install_requires=[
        'pylexibank>=2.1',
    ]
)
