import pathlib

import attr
from clldutils.misc import slug
from pylexibank import Cognate, Language, progressbar, Dataset as BaseDataset

DATAFILE = 'turkic_alignment.tsv'

@attr.s
class CustomCognate(Cognate):
    Root = attr.ib(default=None)

@attr.s
class CustomLanguage(Language):
    Source = attr.ib(default=None)


class Dataset(BaseDataset):
    id = 'savelyevturkic'
    dir = pathlib.Path(__file__).parent
    cognate_class = CustomCognate
    language_class = CustomLanguage

    def cmd_download(self, args):
        self.raw_dir.download(
            "https://zenodo.org/record/3555174/files/turkic_alignment.tsv?download=1",
            'turkic_alignment.tsv',
            log=args.log,
        )

    def cmd_makecldf(self, args):
        args.writer.add_sources()
        sources = {}
        for language in self.languages:
            sources[language["ID"]] = [
                x.lower() for x in language['Source'].split(',')
            ]
            args.writer.add_language(**language)
        segments = {
            "ž": "ʒ",
            "nˈ": "nʲ",
            "lˈ": "lʲ",
            "gˈ": "gʲ",
            "rˈ": "rʲ",
            "pˈ": "pʲ",
            "s-": "s",
            "š": "ʃ",
            "βˈ": "βʲ",
            "sˈ": "sʲ",
            "tʃ": "tɕ",
            "ʦ": "ts",
            "_": "+"
        }
        concepts = args.writer.add_concepts(
            id_factory=lambda x: x.id.split('-')[-1]+"_"+slug(x.english),
            lookup_factory='Name')

        for row in progressbar(self.raw_dir.read_csv(DATAFILE, delimiter="\t", dicts=True)):
            if row['ID'].startswith("#"):
                # skip lingpy stuff
                continue
            
            # patch two weird/broken entries:
            if row['ID'] == '7560':
                row['TOKENS'] = 'ɕ i v ɘ ʨ'
            
            if row['ID'] == '8367':
                row['ENTRY'] = 'ʒɯl'
                
            segs = [segments.get(x, x) for x in row['TOKENS'].split()]
            
            lex = args.writer.add_form_with_segments(
                Local_ID=row['ID'],
                Language_ID=row['DOCULECT'],
                Parameter_ID=concepts.get(row['CONCEPT']),
                Value=row['ENTRY'],
                # sometimes the FORM value is empty for some reason. 
                # if so we use the parsed 'segments' field by removing spaces.
                Form=row['FORM'] if row['FORM'] else "".join(segs),
                Segments=segs,
                Source=sources.get(row['DOCULECT']) or ['']
            )
            args.writer.add_cognate(
                lexeme=lex,
                Cognateset_ID=row['COGID'],
                Alignment=[segments.get(x, x) for x in row['ALIGNMENT']],
                Root=row['ROOT']
            )
