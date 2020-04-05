"""
Convert data to nexus
"""

from lingrex.copar import CoPaR
from lingpy import *
from lingpy.sequence.sound_classes import token2class
from lexibank_savelyevturkic import Dataset
from pylexibank.cli_util import add_dataset_spec
from lingpy.algorithm import misc

def register(parser):
    parser.add_argument(
            '--no-vowels',
            action='store_true',
            help='only look at consonants',
            default=False)
    parser.add_argument(
            '--no-gaps',
            action='store_true',
            help='ignore gaps',
            default=False)
    parser.add_argument(
            '--threshold',
            action='store',
            help='threshold for occurrence of a pattern',
            type=int,
            default=1)
    parser.add_argument(
            '--reflexes',
            action='store',
            help='minimal number of reflexes',
            type=int,
            default=3)
    parser.add_argument(
            '--file',
            action='store',
            help='minimal number of reflexes',
            default='wordlist-correspondences.tsv')



def run(args):

    ds = Dataset()
    cop = CoPaR(ds.dir.joinpath('analysis', args.file).as_posix(), 
            ref='cogid',
            fuzzy=False,
            transcription='form',
            structure='structure')
    #cop.load_patterns()
    cop.get_sites(minrefs=args.reflexes, structure='structure')
    cop.cluster_sites()
    args.log.info('[i] loaded the patterns')
    
    matrix = []
    classes = set()
    for (_, k), vals in cop.clusters.items():
        if len(vals) >= args.threshold:
            for c in [x for x in k if x not in '-Ø']:
                classes.add(token2class(c, 'asjp'))
    
    args.log.info('[i] found {0} sounds in the data'.format(len(classes)))
    sounds = sorted(classes) + ['-']
    new_sounds = '0123456789ABCDEFGHKLMNPQRSTUVWXYZabcdefghklmnpqrstuvwxyz'
    sound_converter = dict(zip(sounds, new_sounds))
    
    for (_, k), vals in cop.clusters.items():
        skip = False
        if len(vals) >= args.threshold and not skip:
            matrix += [[token2class(x, 'asjp') if x not in '-Ø' else '?' if x == 'Ø' else '-' for x in k]]

    

    text = '{0} {1}\n'.format(len(matrix[0]), len(matrix))
    for i in range(len(matrix[0])):
        text += '{0:30}'.format(cop.cols[i])+'   '
        for j in range(len(matrix)):
            text += sound_converter.get(
                    matrix[j][i],
                    matrix[j][i])
        text += '\n'
    
    with open('analysis/{0}-{1}-{2}.phy'.format(args.file[:-4],
        args.threshold,
        args.no_gaps), 'w') as f:
        f.write(text)
    args.log.info("[i] the matrix is {0} and {1}".format(
        len(matrix[0]), len(matrix)))
    with open('analysis/{0}-{1}-{2}.csv'.format(args.file[:-4],
        args.threshold,
        args.no_gaps), 'w') as f:
        matrix = misc.transpose(matrix)
        for i, tax in enumerate(cop.cols):
            f.write(tax+','+','.join(matrix[i])+'\n')



