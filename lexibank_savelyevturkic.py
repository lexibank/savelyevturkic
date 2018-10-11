# coding=utf-8
from __future__ import unicode_literals, print_function

import attr
from clldutils.path import Path
from clldutils.misc import slug
from csvw.dsv import reader
from pylexibank.dataset import Cognate, Dataset as BaseDataset


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
        """
        Convert the raw data to a CLDF dataset.

        Use the methods of `pylexibank.cldf.Dataset` after instantiating one as context:

        >>> with self.cldf as ds:
        ...     ds.add_sources(...)
        ...     ds.add_language(...)
        ...     ds.add_concept(...)
        ...     ds.add_lexemes(...)
        """
        with self.cldf as ds:
            ds.add_languages()
            index2lang = {}
            meaning, root_index = None, 0
            for i, row in enumerate(reader(self.raw / 'Savelyev_Turkic.Sheet1.csv')):
                if i == 0:
                    for j, col in enumerate(row):
                        if (j > 1) and col:
                            index2lang[j] = slug(col)
                elif i > 1:
                    has_cognates = False
                    if row[0]:
                        meaning = '{0}_l{1}'.format(slug(row[0]), i + 1)
                        root_index = 1
                        ds.add_concept(ID=meaning, Name=row[0])
                    else:
                        root_index += 1
                    root = row[1]
                    for j, col in enumerate(row):
                        if col and (j - 1 in index2lang):
                            for lex in ds.add_lexemes(Value=col, Language_ID=index2lang[j - 1], Parameter_ID=meaning):
                                ds.add_cognate(
                                    lexeme=lex,
                                    root=root,
                                    Cognateset_ID='%s-%s-l%s' % (meaning, root_index, i + 1))
                                has_cognates = True
                    if not has_cognates:
                        print(i + 1)
