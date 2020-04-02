"""
Search for correspondence patterns.
"""
from lingpy import *
from lexibank_savelyevturkic import Dataset
from collections import defaultdict
from itertools import combinations
from matplotlib import pyplot as plt
from lingpy.sequence.sound_classes import token2class

def run(args):
    
    ds = Dataset()

    alms = Alignments(ds.raw_dir.joinpath('turkic_alignment.tsv').as_posix(),
            ref='cogid', transcription='form')

    scores = defaultdict(int)
    sounds = defaultdict(int)
    for cogid, msa in alms.msa['cogid'].items():
        for (i, tA), (j, tB) in combinations(enumerate(msa['taxa']), r=2):
            for soundA, soundB in zip(msa['alignment'][i],
                    msa['alignment'][j]):
                scores[soundA, soundB] += 1
                scores[soundB, soundA] += 1
                sounds[soundA] += 1
                sounds[soundB] += 1
    print(len(scores), len(sounds), max(scores.values()))
    matrix = [[0 for x in sounds] for y in sounds]
    soundlist = sorted(sounds, key=lambda x: (
        token2class(x, 'cv', cldf=True),
        token2class(x, 'dolgo', cldf=True),
        token2class(x, 'sca', cldf=True),
        token2class(x, 'asjp', cldf=True)), reverse=True)
    for (i, soundA), (j, soundB) in combinations(enumerate(soundlist), r=2):
        score = scores[soundA, soundB]
        freqA, freqB = sounds[soundA], sounds[soundB]
        score = score / min(freqA, freqB)
        matrix[i][j] = matrix[j][i] = score
    for i, sound in enumerate(soundlist):
        score = scores[sound, sound]
        freq = sounds[sound]
        matrix[i][i] = score/freq
    args.log.info('calculated the matrix')
    plt.imshow(matrix, cmap='jet')
    plt.title('Sound correspondence frequency across Turkic languages')
    cb = plt.colorbar()
    cb.set_label('Frequency')
    plt.xticks(range(0, len(soundlist)), soundlist, fontsize=3)
    plt.yticks(range(0, len(soundlist)), soundlist, fontsize=3)
    plt.savefig(ds.dir.joinpath('output', 'plots.pdf').as_posix())

