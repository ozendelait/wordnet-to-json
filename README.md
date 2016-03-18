WordNet in JSON Format
======================

Such fun!

Download
--------

[Here](https://dl.dropboxusercontent.com/u/20957649/wordnet/wordnet.json.gz).

File Structure
--------------

#### WordNet (root object)

An entire WordNet database.

Fields:

* **Synset** (map to [Synset](#synset)) from synset ID to synset object.
* **Lemma** (map to string array) from pos.lemma to synset IDs that contain it.
* **Exception** (map to string array) from exceptional word to its forms.
* **Example** (map to string) from example ID to sentence template.

#### Synset

A set of synonymous words.

Fields:

* **Pos** (string) part of speech - a, n, r, s, v.
* **Word** (string array) words in this synset
* **Pointer** ([Pointer](#pointer) array) pointers to other synsets.
* **Frame** ([Frame](#frame) array) sentence frames for verbs.
* **Gloss** (string) lexical definition.
* **Example** ([Example](#example) array) usage examples for words in this synset. Verbs only.

#### Pointer

Denotes a semantic relation between one synset/word to another.

Fields:

* **Symbol** (string) relation between the 2 words. Target is \<symbol\> to source. See their meanings
  [here](https://godoc.org/github.com/fluhus/gostuff/nlp/wordnet#pkg-constants).
* **Synset** (string) target synset ID.
* **Source** (int) index of word in source synset, -1 for entire synset.
* **Target** (int) index of word in target synset, -1 for entire synset.

#### Frame

Links a synset word to a generic phrase that illustrates how to use it. Applies to verbs only.

Fields:

* **WordNumber** (int) index of word in the containing synset, -1 for entire synset.
* **FrameNumber** (int) frame number on the WordNet site.

#### Example

Links a synset word to an example sentence. Applies to verbs only.

Fields:

* **WordNumber** (int) index of word in the containing synset, -1 for entire synset.
* **TemplateNumber** (int) tumber of template in the [WordNet](#wordnet).Example field.

Go API
------

If you are working with Go, I encourage you to skip this JSON file and work
directly with the [Go API](https://godoc.org/github.com/fluhus/gostuff/nlp/wordnet).
This JSON dump is simply a serialized
[WordNet](https://godoc.org/github.com/fluhus/gostuff/nlp/wordnet#WordNet)
struct.

Citation
--------

This dataset is based on: Princeton University "About WordNet." WordNet.
Princeton University. 2010. http://wordnet.princeton.edu

Please cite them if you use this dataset.
