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


    def cmd_install(self, **kw):

        modified = {"ž": "ʒ", "nˈ": "nʲ", "lˈ": "lʲ", "gˈ": "gʲ",
                "rˈ": "rʲ", "pˈ": "pʲ", "s-": "s", "š": "ʃ", "βˈ": "βʲ",
                "sˈ": "sʲ", "tʃ": "tɕ", "ʦ": "ts"}


        with self.cldf as ds:
            l2s = {}
            for l in self.languages:
                ds.add_language(ID=l['ID'], Glottolog=l['Glottolog'], 
                        Name=l['Name'])
                l2s[l['ID']] = [x.lower(0 for x in l['Source'].split(',')]
            
            ds.add_sources(*self.raw.read_bib())

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
                        Segments=[modified.get(x, x) for x in wl[idx,
                            'tokens']],
                        Source=l2s[wl[idx, 'doculect']]
                        ):
                    ds.add_cognate(
                            lexeme=lex,
                            Cognateset_ID=wl[idx, 'cogid'],
                            Alignment=[modified.get(x, x) for x in wl[idx,
                                'alignment']]
                            )



