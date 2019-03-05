#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, argparse, json, csv

def json_to_mapping(syn0, entry, word_to_syn, syn_to_syn, syn_missing):
    text0 = entry.get('gloss','').strip().replace(",",";").replace("plies back","flies back")
    word0 =  "&".join(entry['word']).replace('-','_')
    wordkey = word0+'#'+text0
    wordkey_weak = "&"+entry['word'][0].replace('-','_')
    wordkeys = [wordkey,wordkey_weak]
    text0_first = text0
    if '&old(a)' in wordkey:
        word0 = word0.replace('&old(a)','')
        wordkeys.append(word0+'#'+text0)
    if '"' in text0:
        wordkeys.append(word0+'#'+text0.split('"')[-2])
    if '(' in text0:
        text0 = text0.replace('(','').replace(')','')
        wordkeys.append(word0+'#'+text0)
    if ';' in text0:
        text0_first = text0.split(';')[0]
        wordkeys.append(word0+'#'+text0_first)
        wordkeys.append(word0+'#'+text0.replace(';',''))
    if '_' in entry['word'][0] or '-' in entry['word'][0] and len(entry['word']) > 1:
        wordkeys.append("&"+entry['word'][0].replace('-','_'))
        wordkeys.append("&"+entry['word'][0].replace('-','_')+'#'+text0_first)
    wordkeys.append(":"+text0)
    if not syn_to_syn is None: #second pass syn<->syn
        found_key = False
        for w in wordkeys:
            if w in word_to_syn and not word_to_syn[w] is None:
                assert syn0 not in syn_to_syn
                syn_to_syn[syn0] = word_to_syn[w]
                found_key = True
                break
        if not found_key:
            syn_missing[syn0] = ",".join(entry['word'])+": "+ entry['gloss']
    else:
        for w in wordkeys:
            if w in word_to_syn:
                word_to_syn[w] = None #this mapping is not unique -> reject both
            else:
                word_to_syn[w] = syn0

def match_weak(syn_missing, syn_to_syn_weak, red_len = 99, len_txt = 0):
    word_to_syn_weak = []
    for idx in range(len(syn_missing)):
        word_to_syn_weak_loc = {}
        for syn, txt in syn_missing[idx].iteritems():
            syn0 = txt.split(':')
            key0 = syn0[0].strip().replace(' ','').replace('-','_')               
            wordkeys = [key0]
            key0Spl = key0.split(',')
            txt0 = syn0[1].strip().replace('(','').replace(')',' ')
            len_txt0 = min(len_txt, len(txt0))
            if len(key0Spl) > red_len:
                wd0, wd1 = "", "" 
                for i in range(0,min(red_len,len(key0Spl))):
                    wd0 += key0Spl[i]+','
                for i in range(max(0,len(key0Spl)-red_len),len(key0Spl)):
                    wd1 += key0Spl[i]+','
                wordkeys.append(wd0[:-1])
                wordkeys.append(wd1[:-1])
                if len_txt0 > 8:
                    wordkeys.append(wd0[:-1]+txt0[:len_txt0])
                    wordkeys.append(wd1[:-1]+txt0[len(txt0)-len_txt0+1:])
            elif len_txt0 > 8:
                wordkeys.append(key0+txt0[:len_txt0])
                wordkeys.append(key0+txt0[len(txt0)-len_txt0+1:])
            if len_txt0 > 8:
                wordkeys.append(txt0[:len_txt0])
                wordkeys.append(txt0[len(txt0)-len_txt0+1:])
            for w in wordkeys:
                if w in word_to_syn_weak_loc:
                    word_to_syn_weak_loc[w] = None #this mapping is not unique -> reject both
                else:
                    word_to_syn_weak_loc[w] = syn
        word_to_syn_weak.append(word_to_syn_weak_loc)
    for word,syn in word_to_syn_weak[0].iteritems():
        if syn is None:
            continue
        if word in word_to_syn_weak[1] and not word_to_syn_weak[1][word] is None:
            syn_to_syn_weak[0][syn] = word_to_syn_weak[1][word]
            syn_to_syn_weak[1][word_to_syn_weak[1][word]] = syn
            syn_missing[0].pop(syn, None)
            syn_missing[1].pop(word_to_syn_weak[1][word], None)

def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--wordnet_src', type=str, default="wordnet_v3p1.json",
                    help='Path to json file containing source wordnet labels')
    parser.add_argument('--wordnet_trg', type=str, default="wordnet_v3p0.json",
                    help='Path to json file containing destination wordnet labels')
    parser.add_argument('--imagenettxt', type=str, default="imagenet1000_clsid_to_labels.txt",
                    help='Path to json file containing imagenet labels')
    parser.add_argument('--output', type=str, default="mapping_wordnet.json",
                        help="Output json file path")
    args = parser.parse_args(argv)
        
    mapping =  [{'wordnet_version_from':3.1,'wordnet_version_to':3.0},{'wordnet_version_from':3.0,'wordnet_version_to':3.1}] #TODO make configurable/extract from filename
    word_to_syn = [] # temp. structure holding src/trg word string -> synset
    jsoncont = []
    #first load word_to_syn dicts
    for idx, jsonpath in enumerate([args.wordnet_trg,args.wordnet_src]):
        jsoncont_loc = json.load(open(jsonpath, 'r'))
        word_to_syn_loc ={}
        for synsetid, entry in jsoncont_loc['synset'].iteritems():
            json_to_mapping(synsetid, entry, word_to_syn_loc, None, None)
        word_to_syn.append(word_to_syn_loc)
        jsoncont.append(jsoncont_loc)
        
    syn_to_syn = [] # will hold final synset mappings
    syn_missing = [] # holds missing mappings (word in one file but not the other)
    jsoncont.reverse() #now switch roles, fill syn_to_syn dicts
    word_to_syn_weak = []
    for idx, jsoncont_loc in enumerate(jsoncont):
        word_to_syn_loc = word_to_syn[idx]
        syn_to_syn_loc = {}
        syn_missing_loc = {}
        for synsetid, entry in jsoncont_loc['synset'].iteritems():
            json_to_mapping(synsetid, entry, word_to_syn_loc, syn_to_syn_loc, syn_missing_loc)
        syn_to_syn.append(syn_to_syn_loc) 
        syn_missing.append(syn_missing_loc)
    
    syn_to_syn_weak = [{},{}]
    last_count_missing = len(syn_missing)+1
    while len(syn_missing) > 0 and len(syn_missing) < last_count_missing:
        last_count_missing = len(syn_missing)
        match_weak(syn_missing, syn_to_syn_weak)
        match_weak(syn_missing, syn_to_syn_weak, len_txt = 32)
        match_weak(syn_missing, syn_to_syn_weak, red_len = 3)
        match_weak(syn_missing, syn_to_syn_weak, red_len = 2)
        match_weak(syn_missing, syn_to_syn_weak, red_len = 1)
        match_weak(syn_missing, syn_to_syn_weak, red_len = 2, len_txt = 12)
    
    #fix missing links:
    #for idx0 in enumerate(syn_missing):
    #    idx1 = 1-idx0
    #    for s in syn_missing[idx0]:
    #        cmpWords = word_to_syn[idx1]
    #        if "_" in cmpWords or "-" in cmpWords:        

    for idx in range(len(mapping)):
        cnt_same_offsets = 0
        for k,v in syn_to_syn[idx].iteritems():
            if int(k[1:]) == int(v[1:]):
                cnt_same_offsets += 1
        
        mapping[idx]['count-synset'] = len(syn_to_syn[idx])
        mapping[idx]['count-synset-weak'] = len(syn_to_syn_weak[idx])
        mapping[idx]['count-sysnet-same-offset'] = cnt_same_offsets
        mapping[idx]['count-missing'] = len(syn_missing[idx])
        mapping[idx]['synset-mapping'] = syn_to_syn[idx]
        mapping[idx]['synset-weak-mapping'] = syn_to_syn_weak[idx]
        mapping[idx]['synset-missing'] = syn_missing[idx]

    with open(args.output, 'w') as ofile:
        json.dump(mapping, ofile, sort_keys=True, indent=4)
        
    if args.imagenettxt != "":
        jsoncont_imgnet = []
        with open(args.imagenettxt, 'r') as imgnettxt:
            for idx,f in enumerate(imgnettxt):
                splSem = f.split(':')
                idv30 = splSem[0].replace('}','').replace('{','').strip()
                idv31 = syn_to_syn[1].get(idv30,None)
                if idv31 is None:
                    idv31 = syn_to_syn_weak[1].get(idv30,None)
                assert idv31 is not None
                text_desc = splSem[1].strip()[1:-1]
                jsoncont_imgnet.append({'idx': idx, 'v3p0':idv30, 'v3p1':idv31, 'label':text_desc})
        with open(args.output+"imgnet.json", 'w') as ofile:
            json.dump(jsoncont_imgnet, ofile, sort_keys=True, indent=4)
if __name__ == "__main__":
    print("Automatically generate mapping between ids of wordnet versions 3.0 and 3.1 (both ways)")
    sys.exit(main())
