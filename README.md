WordNet v3.0 vs. v3.1 mapping
======================

Based on the converter from https://github.com/fluhus/wordnet-to-json; 
Applied to wordnet v3.0 data to create json compatible with ImageNet synset ids.
Created semi-automatic mapping v3.1 <-> v3.0 (only about 100 entries of 1286600 could not be matched)

# Statistics from mapping synset v3.1 <-> v3.0:  
| # synset      | v3.1->v3.0    | v3.0->v3.1   |
| ------------- |:-------------:| -----:|
| worked      | 117278 | 117264 |
| weakly linked     | 305      |   302 |
| missing | 208      |    93 |
| same offset | 58      |    58 |


Note: the official Wordnet search-engine allows switching to v3.0 (see answer from Finn Årup Nielsen:
https://stackoverflow.com/questions/45826417/imagenet-index-to-wordnet-3-0-synsets
; e.g. http://wordnet-rdf.princeton.edu/pwn30/01440764-n ).
There is currently no reason to use v3.1 if you work with ImageNet. Just stick to v3.0.

Citation
--------

This dataset is based on: Princeton University "About WordNet." WordNet.
Princeton University. 2010. http://wordnet.princeton.edu
Please cite them if you use this dataset.

The original converter script has been written by Amit Lavon (Github user fluhus https://github.com/fluhus ).

If you find the mapping files (mapping_wordnet.json or mapping_imagenet.json) useful, please cite this repo:

    @misc{ZendelWordNetConv19,
      author = {Zendel, Oliver},
      title = {WordNet v3.0 vs. v3.1 mapping},
      year = {2019},
      publisher = {GitHub},
      journal = {GitHub repository},
      howpublished = {\url{https://github.com/ozendelait/wordnet-to-json}},
      commit = {7521b70937355e826ea7e028a615108cdb18d0ee}
    }

Download
--------

Mapping files:
mapping_wordnet.json: https://raw.githubusercontent.com/ozendelait/wordnet-to-json/master/mapping_wordnet.json
mapping_imagenet.json: https://raw.githubusercontent.com/ozendelait/wordnet-to-json/master/mapping_imagenet.json

WordNet v3.0: See [releases](https://github.com/ozendelait/wordnet-to-json/releases/download/wordnet-v3.0/wordnet.json.gz).
WordNet v3.1: See (https://github.com/fluhus/wordnet-to-json/releases).
ImageNet subset (original, no v3.1 info): See https://gist.github.com/yrevar/667fd94b94f1666137f45d1363f60910
