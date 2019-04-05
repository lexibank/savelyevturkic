# coding=utf-8
from __future__ import unicode_literals, print_function

import attr
from clldutils.path import Path
from clldutils.misc import slug
from csvw.dsv import reader
from pylexibank.dataset import Cognate, NonSplittingDataset as BaseDataset
from lingpy import *
from pylexibank.util import pb


@attr.s
class TurkicCognate(Cognate):
    root = attr.ib(default=None)


class Dataset(BaseDataset):
    id = 'savelyevturkic'
    dir = Path(__file__).parent
    cognate_class = TurkicCognate

    def cmd_download(self, **kw):
        self.raw.xls2csv('Savelyev_Turkic.xls')

    def _read(self, what):
        return reader(self.raw / '{0}.tsv'.format(what), dicts=True, delimiter='\t')

    def cmd_install(self, **kw):
        with self.cldf as ds:
            ds.add_languages(id_factory=lambda l: l['ID'])
            
            wl = Wordlist(self.raw.posix('turkic_alignment.tsv'))
            for concept in self.concepts:
                ds.add_concept(
                        ID=slug(concept['ENGLISH']),
                        Name=concept['ENGLISH'],
                        Concepticon_ID=concept['CONCEPTICON_ID']
                        )

            for idx in pb(wl):
                for lex in ds.add_lexemes(
                        Language_ID=wl[idx, 'doculect'],
                        Parameter_ID=slug(wl[idx, 'concept']),
                        Value=wl[idx, 'entry'],
                        Form=wl[idx, 'form'],
                        Segments=wl[idx, 'tokens'],
                        Source=''
                        ):
                    ds.add_cognate(
                            lexeme=lex,
                            Cognateset_ID=wl[idx, 'cogid'],
                            Alignment=wl[idx, 'alignment']
                            )



