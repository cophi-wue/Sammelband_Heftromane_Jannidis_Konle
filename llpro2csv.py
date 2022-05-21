"""
    converts output from the llpro pipeline into a csv file
"""

import csv
import json
from pathlib import Path
import argparse    
import tqdm
    
def ner(line):
    #handles named entities (come in lists)
    if len(line['ner']['FLERTNERTagger']) > 0:
        return line['ner']['FLERTNERTagger'][0]
    else:
        return ' '

def coref(line):
    """
    handles coref clusters. at the moment only the first cluster reference is included
    """
    if len(line['coref_clusters']['CorefIncrementalTagger']) > 0:        
        return line['coref_clusters']['CorefIncrementalTagger'][0]       
    else:
        return '-1'

def rw(line):
    """
    reformats the output of the redewiedergabe tool
    """
    if len(line['redewiedergabe']['RedewiedergabeTagger']) > 0:
        return '-'.join(line['redewiedergabe']['RedewiedergabeTagger'])
    else: 
        return ' '

def write_csv_row(writer, line):
    """writes a row in cvs file

    Args:
        writer (cvs.writer): the cvs file writer
        line (json): one line of output from llpro
    """
    writer.writerow({'id': line['id']['NLTKPunktTokenizer'],
                     'sentence': line['sentence']['NLTKPunktTokenizer'],
                     'word': line['word']['NLTKPunktTokenizer'],
                     'lemma_rnn': line['lemma']['RNNLemmatizer'],
                     'lemma_parzu': line['lemma']['ParzuParser'],
                     'pos_sow':  line['pos']['SoMeWeTaTagger'],  
                     'pos_rnn': line['pos']['RNNTagger'],              
                     'pos_par': line['pos']['ParzuParser'], 
                     'morph_rnn': line['morph']['RNNTagger'],
                     'morph_parzu': line['morph']['ParzuParser'],
                     'ner': ner(line),
                     'coref_cluster': coref(line),
                     'redewiedergabe': rw(line),
                     'srl': line['srl']['InVeRoXL'],
                     'head': line['head']['ParzuParser'],       
                     'dependency': line['deprel']['ParzuParser']                                    

                    })
    


def write_csv(infile, out_dir, out_file):
    with open(Path(out_dir) / out_file, 'w', newline='') as csvfile:
        fieldnames = ['id','sentence','word','lemma_rnn','lemma_parzu', 'pos_sow','pos_rnn','pos_par','morph_rnn',
                      'morph_parzu','ner','coref_cluster', 'redewiedergabe','srl','head','dependency'] #,,
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        
        with open(infile) as fin:
            for line in fin:
                write_csv_row(writer, json.loads(line))


def convert(args):
    files = list(Path(args.indir).glob('*')) + list(Path(args.indir).glob('*.*'))
    for file in tqdm.tqdm(files):
        #write_csv(file, args.outdir, file.name)
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts LLPro output to a cvs file.')    
    parser.add_argument('--indir', '-i', help='input directory', required=True)    
    parser.add_argument('--outdir', '-o', help='output directory', required=True)    
    args = parser.parse_args()
    convert(args)
    
    
        
