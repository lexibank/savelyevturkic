import attr
from pathlib import Path
from clldutils.misc import slug
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank import Cognate, Language
from lingpy import *
from pylexibank import progressbar


@attr.s
class CustomCognate(Cognate):
    Root = attr.ib(default=None)

@attr.s
class CustomLanguage(Language):
    Source = attr.ib(default=None)


class Dataset(BaseDataset):
    id = 'savelyevturkic'
    dir = Path(__file__).parent
    cognate_class = CustomCognate
    language_class = CustomLanguage

    def cmd_download(self, args):
        self.raw_dir.download(
                "https://zenodo.org/record/3555174/files/turkic_alignment.tsv?download=1",
                'turkic_alignment.tsv'
                )

    def cmd_makecldf(self, args):

        args.writer.add_sources()
        sources = {}
        for language in self.languages:
            sources[language["ID"]] = [x.lower() for x in
                    language['Source'].split(',')]
            args.writer.add_language(**language)
        segments = {"ž": "ʒ", "nˈ": "nʲ", "lˈ": "lʲ", "gˈ": "gʲ",
                "rˈ": "rʲ", "pˈ": "pʲ", "s-": "s", "š": "ʃ", "βˈ": "βʲ",
                "sˈ": "sʲ", "tʃ": "tɕ", "ʦ": "ts"}
        concepts = args.writer.add_concepts(
                id_factory=lambda x: x.id.split('-')[-1]+"_"+slug(x.english),
                lookup_factory='Name')

        wl = Wordlist(self.raw_dir.joinpath('turkic_alignment.tsv').as_posix())
        for idx in progressbar(wl):
            lex = args.writer.add_form_with_segments(
                    Language_ID=wl[idx, 'doculect'],
                    Parameter_ID=concepts[wl[idx, 'concept']],
                    Value=wl[idx, 'entry'] or 'NAN',
                    Form=wl[idx, 'form'] or 'NAN',
                    Segments=[segments.get(x, x) for x in wl[idx,
                        'tokens']],
                    Source=sources[wl[idx, 'doculect']] or ['']
                    )
            args.writer.add_cognate(
                    lexeme=lex,
                    Cognateset_ID=wl[idx, 'cogid'],
                    Alignment=[segments.get(x, x) for x in wl[idx, 'alignment']],
                    Root=wl[idx, 'root']
                    )



