"""
Search for correspondence patterns.
"""
from lingrex.copar import CoPaR
from lingpy import *
from lexibank_savelyevturkic import Dataset


def run(args):
    
    ds = Dataset()

    wl = Wordlist.from_cldf(ds.dir.joinpath('cldf', 'cldf-metadata.json'),
            columns=('parameter_id', 'concept_name', 'language_id',
                'language_name', 'value', 'form', 'segments',
                'cogid_cognateset_id'))
    D = {0: wl.columns}
    for idx in wl:
        if not wl[idx, 'tokens']:
            pass
        else:
            D[idx] = wl[idx]

    alms = Alignments(D, ref='cogid', transcription='form', segments='tokens')
    alms.align()

    cop = CoPaR(
            alms,
            ref='cogid',
            fuzzy=False,
            segments='tokens',
            transcription='form'
            )
    cop.add_structure(model='cv')
    cop.get_sites(minrefs=3, structure='structure')
    cop.cluster_sites()
    cop.sites_to_pattern()
    cop.add_patterns()
    cop.write_patterns(ds.dir.joinpath('analysis', 'correspondence-patterns.tsv').as_posix())
    cop.output('tsv', filename=ds.dir.joinpath('analysis',
        'wordlist-correspondences').as_posix(), prettify=False, ignore='all')
    



